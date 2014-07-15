import sys
from .base import Action
from util import LIST_FORMAT


class ListAction(Action):

    def __init__(self, args):
        super().__init__(args, 'GET')
        self.fields = ['name', 'type', 'log_level', 
                       'auto_start', 'sys_metadata', 'mappings']

    def _create_url(self):
        urls = []
        for n in self.args.name:
            url = LIST_FORMAT.format(self.args.host, self.args.port, 
                                     self.args.resource, n)
            if self.args.cmd:
                url += '/commands'
            urls.append(url)

        return urls or [LIST_FORMAT.format(self.args.host, self.args.port,
                                           self.args.resource, '')]
        
    def _process_rsp(self, rsp):
        data = rsp.json()
        rows = []
        if self.args.cmd and self.args.name:
            rows = self._gen_command_list(data)
        elif self.args.name:
            rows = self._gen_spec(data)
        else:
            rows = self._gen_list(data)

        if sys.stdout.isatty():
            print(self._get_table(rows))
        else:
            # note that, if we list a specific block/service for not a tty,
            # we don't get the name.
            for r in rows[1:]:
                print(self._format_line(r))
