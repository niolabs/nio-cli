import subprocess
from nio_cli.actions.base import Action
from nio_cli.util import NIOClient, try_int

class ServerAction(Action):

    def __init__(self, args):
        super().__init__(args)
        self.executable = args.exec

    def perform(self):
        with subprocess.Popen([self.executable]) as proc:
            try:
                while proc.poll() is None:
                    continue
            except:
                pass
