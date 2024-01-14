import time
import typing
import bittensor as bt
from ...niche_image_subnet.base import BaseMinerNeuron
from ... import niche_image_subnet as ni_subnet


class Miner(BaseMinerNeuron):
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)
        self.validator_logs = {}
        self.miner_info = ni_subnet.miner.set_info(self)

    async def forward(
        self, synapse: ni_subnet.protocol.ImageGenerating
    ) -> ni_subnet.protocol.ImageGenerating:
        bt.logging.info(f"synapse {synapse}")

        if synapse.prompt:
            image = ni_subnet.miner.generate(
                self, synapse.prompt, synapse.seed, synapse.pipeline_params
            )
            synapse.image = image

        if synapse.request_dict:
            synapse.response_dict = self.miner_info
            bt.logging.info(f"Response dict: {self.miner_info}")
        return synapse

    async def blacklist(
        self, synapse: ni_subnet.protocol.ImageGenerating
    ) -> typing.Tuple[bool, str]:
        bt.logging.info(f"synapse in blacklist {synapse}")

        if synapse.dendrite.hotkey not in self.metagraph.hotkeys:
            # Ignore requests from unrecognized entities.
            bt.logging.trace(
                f"Blacklisting unrecognized hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        validator_uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        stake = self.metagraph.stake[validator_uid].item()

        if ni_subnet.miner.check_min_stake(stake, validator_uid):
            bt.logging.trace(
                f"Blacklisting {validator_uid}-validator has {stake} stake"
            )
            return True, "Not enough stake"
        if ni_subnet.miner.check_limit(self, uid=validator_uid, stake=stake):
            bt.logging.trace(
                f"Blacklisting {validator_uid}-validator for exceeding the limit"
            )
            return True, "Limit exceeded"

        return False, "All passed!"

    async def priority(self, synapse: ni_subnet.protocol.ImageGenerating) -> float:
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        prirority = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: ", prirority
        )
        return prirority


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)
