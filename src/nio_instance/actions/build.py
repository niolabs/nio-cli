import sys
import requests
from .base import Action
from util import LIST_FORMAT, Execution, NIOClient


class BuildAction(Action):
    
    def _create_url(self):
        return [LIST_FORMAT.format(self.args.host, self.args.port,
                                   'services', self.args.name)]
    def perform(self):
        service = NIOClient.list('services', self.args.name).json()
        service_exec = Execution(service['execution'])

        for l in self.args.edges:
            frm, to = l
            if self.args.rm:
                service_exec.rm_edge(frm, to)
            else:
                service_exec.add_edge(frm, to)

        service['execution'] = service_exec.pack()
        NIOClient.build(self.args.name, service)

        self.generate_output(service_exec)

    def generate_output(self, service_exec):
        rows = self._gen_execution_list(service_exec.edges)
        super().generate_output(rows)

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
