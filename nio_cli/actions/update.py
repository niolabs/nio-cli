from nio_cli.actions.base import Action
from nio_cli.util import NIOClient


class UpdateAction(Action):

    def perform(self):
        for blk in self.args.block_types:
            NIOClient.update(blk)
