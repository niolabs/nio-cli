import requests
from .base import Action
from util import LIST_FORMAT

class Execution(object):
    def __init__(self, execution):
        self.links = {
            e['name']: e['receivers'] for e in execution
        }
        
    def add_link(self, frm, to):
        frm_curr = self.links.get(frm, [])
        if to not in frm_curr:
            frm_curr.append(to)
        self.links[frm] = frm_curr
            
    def rm_link(self, frm, to):
        frm_curr = self.links.get(frm, [])
        frm_curr = [t for t in frm_curr if t != to]
        self.links[frm] = frm_curr

    def pack(self):
        return [{
            'name': e, 'receivers': self.links[e]
        } for e in self.links]


class LinkAction(Action):
    
    def __init__(self, args):
        super().__init__(args, 'PUT')

    def _create_url(self):
        return [LIST_FORMAT.format(self.args.host, self.args.port,
                                   'services', self.args.name)]
    def perform(self):
        service = requests.get(self.urls[0], auth=self.auth).json()
        service_exec = Execution(service['execution'])
        if len(self.args.links) > 0:
            print(self.args.links)
            for l in self.args.links:
                frm, to = l
                if self.args.rm:
                    service_exec.rm_link(frm, to)
                else:
                    service_exec.add_link(frm, to)
            service['execution'] = service_exec.pack()
            super().perform(service)
        else:
            rows = self._gen_execution_list(service_exec.links)
            print(self._get_table(rows))
