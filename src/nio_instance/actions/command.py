import requests
from .base import Action
from util import COMMAND_FORMAT, SHUTDOWN, LIST_FORMAT


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
            if self.args.interactive:
                data = self._collect_params(data)
            else:
                for a in self.args.args:
                    param, arg = a
                    data[param] = arg

            super().perform(data)

    def _collect_params(self, data):
        prompt="{0} ({1}): "
        url = LIST_FORMAT.format(
            self.args.host, self.args.port,
            'blocks' if self.args.block else 'services',
            self.args.block if self.args.block else self.args.service
        ) + '/commands'
        commands = requests.get(url, auth=self.auth).json()
        command_template = commands.get(self.args.command, {})['params']
        for name in command_template:
            _type = command_template[name]['type']
            result = input(prompt.format(name, _type))
            if _type == 'int':
                result = int(result)
            data[name] = result
        return data
            
    def _process_rsp(self, rsp):
        data = rsp.json()
        print(data)
