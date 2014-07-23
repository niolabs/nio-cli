import sys
import requests
from .base import Action
from util import LIST_FORMAT, Execution


class BuildAction(Action):
    
    def __init__(self, args):
        super().__init__(args, 'PUT')

    def _create_url(self):
        return [LIST_FORMAT.format(self.args.host, self.args.port,
                                   'services', self.args.name)]
    def perform(self):
        service = requests.get(self.urls[0], auth=self.auth).json()
        service_exec = Execution(service['execution'])

        if len(self.args.edges) > 0:
            for l in self.args.edges:
                frm, to = l
                if self.args.rm:
                    service_exec.rm_edge(frm, to)
                else:
                    service_exec.add_edge(frm, to)
            service['execution'] = service_exec.pack()
            super().perform(service)
            
        rows = self._gen_execution_list(service_exec.edges)
        if sys.stdout.isatty():
            print(self._get_table(rows))
        else:
            for r in rows:
                print(self._format_line(r))

    def _gen_execution_list(self, data):
        header = ['Output Block']
        align = []
        rows = [align, header]
        for frm in data:
            rows.append([frm] + data[frm])

        max_len = max([len(r) for r in rows])
        rows[1] += list(range(max_len-1))
        rows[1:] = [r + [''] * (max_len - len(r)) for r in rows[1:]]
        return rows
