import requests
from .base import Action
from util import NIOClient


class CommandAction(Action):

    def __init__(self, args):
        super().__init__(args)
        self.resource = 'blocks' if args.block else 'services'
        self.name = args.block or args.service

    @property
    def params(self):
        if self.args.interactive:
            return self._collect_params()
        else:
            return {a[0]: a[1] for a in self.args.args}

    def perform(self):
        if self.args.command == 'shutdown':
            NIOClient.shutdown()
        elif self.args.command == 'restart':
            NIOClient.command('stop', self.args.service)
            NIOClient.command('start', self.args.service)
        else:
            rsp = NIOClient.command(self.args.command,
                                    self.args.service,
                                    self.args.block,
                                    self.params)
            print(self.process(rsp))

    def _collect_params(self):
        data = {}
        prompt="{0} ({1}): "
        commands = NIOClient.list(self.resource, self.name, True).json()
        command_template = commands.get(self.args.command, {}).get('params')

        for name in command_template:
            _type = command_template[name]['type']
            result = input(prompt.format(name, _type))

            # we currently only have integer and string params for commands
            if _type == 'int':
                result = int(result)

            data[name] = result

        return data
