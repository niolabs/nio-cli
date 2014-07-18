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

    def _gen_spec(self, data):
        block_name = data.get('name')
        excl = ['name', 'execution']
        header = [block_name, '']
        align = [(block_name, 'l')]
        rows = [align, header]
        keys = sorted([k for k in data.keys() if k not in excl])
        for k in keys:
            val = data[k]
            if isinstance(val, dict):
                rows.append([k, ''])
                for kp in val:
                    rows.append(["+-> %s" % kp, val[kp] or "NULL"])
            else:
                rows.append([k, data[k] or "NULL"])
                
        return rows

    def _gen_list(self, data):
        eg = list(data.values())[0]
        header = keys = [k for k in self.fields if k in eg]
        align = [(header[0],'l')]
        rows = [align, header]
        for k in data.keys():
            rows.append([data[k].get(j) for j in keys])
        return rows

    # TODO: refactor these next two methods, most of the code is repeated
    # use your fp skillz, player
    def _gen_command_list(self, data):
        header = ['command']
        align = [(header[0], 'l')]
        rows = [align, header]
        for cmd in data:
            params = data[cmd]['params']
            r = [cmd]
            rows.append([cmd] + ["{0}: ({1})".format(p, params[p]['type']) \
                                 for p in params])

        max_len = max([len(r) for r in rows])
        rows[1] += list(range(max_len-1))
        rows[1:] = [r + [''] * (max_len - len(r)) for r in rows[1:]]
        return rows
