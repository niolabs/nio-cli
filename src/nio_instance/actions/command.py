from .base import Action
from util import COMMAND_FORMAT, SHUTDOWN


class CommandAction(Action):

    def __init__(self, args):
        super().__init__(args, 'POST')
        self.fields = ['title', 'params']

    def _create_url(self):
        result = []
        url = COMMAND_FORMAT.format(self.args.host, self.args.port,
                                    self.args.service, self.args.block)

        if self.args.command == 'restart':
            result.append(url + 'stop')
            result.append(url + 'start')
        else:
            result.append(url + self.args.command)
        return result

    def perform(self):
        if self.args.command == 'shutdown':
            requests.get(SHUTDOWN, auth=self.auth)
        else:
            data = {}
            for a in self.args.args:
                param, arg = a
                data[param] = arg

            super().perform(data)

    def _process_rsp(self, rsp):
        data = rsp.json()
        print(data)
