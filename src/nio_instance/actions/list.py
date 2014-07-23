import sys
from .base import Action
from util import LIST_FORMAT, NIOClient


FIELDS = [
    'name',
    'type',
    'log_level',
    'auto_start',
    'sys_metadata',
    'mappings'
]


class ListAction(Action):

    def perform(self):
        for n in self.args.names:
            rsp = NIOClient.list(self.args.resource, n, self.args.cmd)
            if rsp is not None and rsp.text:
                ls_all = not bool(self.args.names[0])
                self.process(rsp, ls_all)

    def process(self, rsp, ls_all):
        data = rsp.json()
        if ls_all:
            [self.generate_output(data[n]) for n in data]
        else:
            self.generate_output(data)

    def generate_output(self, data):
        rows = self._get_rows(data)
        super().generate_output(rows)

    def _get_rows(self, data):
        ''' Decide which type of table we want based on
        subcommand arguments.

        '''
        if self.args.cmd and self.args.names:
            return self._gen_command_list(data)
        elif self.args.names:
            return self._gen_spec(data)
        else:
            return self._gen_list(data)
