import time
import bittensor as bt
import random
import torch
import traceback
from ...niche_image_subnet.protocol import ImageGenerating
from ...niche_image_subnet.base import BaseValidatorNeuron
from ...niche_image_subnet.validator.forward import get_prompt, get_reward
from ... import niche_image_subnet as ni_subnet
from .validator_proxy import ValidatorProxy


class Validator(BaseValidatorNeuron):
    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        self.all_uids = [int(uid.item()) for uid in self.metagraph.uids]

        bt.logging.info("load_state()")
        self.load_state()

        for uid in self.all_uids:
            if not str(uid) in self.all_uids_info:
                self.all_uids_info[str(uid)] = {"scores": [], "model_name": "unknown"}

        self.supporting_models = {
            "RealisticVision": {
                "incentive_weight": 0.5,
                "checking_url": self.config.realistic_vision.check_url,
                "inference_params": {"num_inference_steps": 30},
                "timeout": 12,
            },
            "SDXLTurbo": {
                "incentive_weight": 0.5,
                "checking_url": self.config.sdxl_turbo.check_url,
                "inference_params": {
                    "num_inference_steps": 4,
                    "width": 512,
                    "height": 512,
                    "guidance_scale": 0.5,
                },
                "timeout": 4,
            },
        }
        self.max_validate_batch = 5

        self.update_active_models_func = ni_subnet.validator.update_active_models

        if self.config.proxy.port:
            try:
                self.validator_proxy = ValidatorProxy(self)
                bt.logging.info("Validator proxy started succesfully")
            except Exception as e:
                bt.logging.warning(
                    "Warning, proxy did not start correctly, so no one can query through your validator. Error message: "
                    + traceback.format_exc()
                )

    def forward(self):
        """
        Validator forward pass. Consists of:
        - Querying all miners to get what model they run
        - Generating the query
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """

        bt.logging.info("Updating available models & uids")
        self.update_active_models_func(self)

        for model_name in self.supporting_models.keys():
            batch_size = random.randint(1, self.max_validate_batch)

            bt.logging.info(f"Validating {model_name} model")

            available_uids = [
                int(uid)
                for uid in self.all_uids_info.keys()
                if self.all_uids_info[uid]["model_name"] == model_name
            ]
            random.shuffle(available_uids)

            if not available_uids:
                bt.logging.warning(
                    "No active miner available for specified model. Skipping setting weights."
                )
                continue
            else:
                bt.logging.info(f"Available uids: {available_uids}")

            num_batch = (len(available_uids) + batch_size - 1) // batch_size

            seeds = [random.randint(0, 1e9) for _ in range(num_batch)]
            batched_uids = [
                available_uids[i * batch_size : (i + 1) * batch_size]
                for i in range(num_batch)
            ]
            prompts = [
                ni_subnet.validator.get_prompt(
                    seed=seeds[i], prompt_url=self.config.prompt_generating_endpoint
                )
                for i in range(num_batch)
            ]
            synapses = [
                ImageGenerating(
                    prompt=prompts[i],
                    seed=seeds[i],
                    model_name=model_name,
                )
                for i in range(num_batch)
            ]
            for synapse in synapses:
                synapse.pipeline_params.update(
                    self.supporting_models[model_name]["inference_params"]
                )

            for synapse, uids in zip(synapses, batched_uids):
                responses = self.dendrite.query(
                    axons=[self.metagraph.axons[uid] for uid in uids],
                    synapse=synapse,
                    deserialize=False,
                )
                # Filter uid, response that blacklisted
                valid_uids = [
                    uid
                    for uid, response in zip(uids, responses)
                    if response.axon.status_code != 403
                ]
                invalid_uids = [
                    uid
                    for uid, response in zip(uids, responses)
                    if response.axon.status_code == 403
                ]
                responses = [
                    response
                    for response in responses
                    if response.axon.status_code != 403
                ]

                bt.logging.info("Received responses, calculating rewards")
                checking_url = self.supporting_models[synapse.model_name][
                    "checking_url"
                ]
                rewards = ni_subnet.validator.get_reward(
                    checking_url, responses, synapse
                )

                bt.logging.info(f"Scored responses: {rewards}")

                for i in range(len(invalid_uids)):
                    uid = str(invalid_uids[i])
                    self.all_uids_info[uid]["scores"].append(0)

                    if len(self.all_uids_info[uid]["scores"]) > 10:
                        self.all_uids_info[uid]["scores"] = self.all_uids_info[uid][
                            "scores"
                        ][-10:]

                for i in range(len(valid_uids)):
                    uid = str(valid_uids[i])
                    self.all_uids_info[uid]["scores"].append(rewards[i])

                    if len(self.all_uids_info[uid]["scores"]) > 10:
                        self.all_uids_info[uid]["scores"] = self.all_uids_info[uid][
                            "scores"
                        ][-10:]

        self.update_scores_on_chain()
        self.save_state()

    def update_scores_on_chain(self):
        """Performs exponential moving average on the scores based on the rewards received from the miners."""

        weights = torch.zeros(len(self.all_uids))

        for model_name in self.supporting_models.keys():
            model_specific_weights = torch.zeros(len(self.all_uids))

            for uid in self.all_uids_info.keys():
                if self.all_uids_info[uid]["model_name"] == model_name:
                    num_past_to_check = 5
                    model_specific_weights[int(uid)] = (
                        sum(self.all_uids_info[uid]["scores"][-num_past_to_check:])
                        / num_past_to_check
                    )

            tensor_sum = torch.sum(model_specific_weights)
            # Normalizing the tensor
            if tensor_sum > 0:
                model_specific_weights = model_specific_weights / tensor_sum
            else:
                continue
            # Correcting reward
            model_specific_weights = (
                model_specific_weights
                * self.supporting_models[model_name]["incentive_weight"]
            )
            bt.logging.info(
                f"model_specific_weights for {model_name}\n{model_specific_weights}"
            )
            weights = weights + model_specific_weights

        # Check if rewards contains NaN values.
        if torch.isnan(weights).any():
            bt.logging.warning(f"NaN values detected in weights: {weights}")
            # Replace any NaN values in rewards with 0.
            weights = torch.nan_to_num(weights, 0)

        self.scores: torch.FloatTensor = weights
        bt.logging.info(f"Updated scores: {self.scores}")


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(60)
