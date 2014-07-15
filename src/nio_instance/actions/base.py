import json
import requests
import sys
from prettytable import PrettyTable


class Action(object):
    def __init__(self, args, cmd):
        self.args = args
        self.urls = self._create_url()
        self.cmd = cmd
        self.auth = ('Admin', 'Admin')

    def perform(self, data=None):
        data = json.dumps(data) if data is not None else data
        for url in self.urls:
            try:
                rsp = requests.request(self.cmd, url, auth=self.auth, data=data)
            except Exception as e:
                print(type(e), e, file=sys.stderr)
                sys.exit(1)
            status = rsp.status_code
            if status == 200:
                if rsp.text:
                    self._process_rsp(rsp)
                else:
                    print('`%s`' % rsp.request.url, "was processed successfully")
            else:
                print("NIO request returned status %d" % status, file=sys.stderr)

    def _process_rsp(self, rsp):
        pass
    
    def _format_line(self, row):
        return ' '.join([str(i) for i in row])

    def _gen_list(self, data):
        eg = list(data.values())[0]
        header = keys = [k for k in self.fields if k in eg]
        rows = [header]
        for k in data.keys():
            rows.append([data[k].get(j) for j in keys])
        return rows


    # TODO: refactor these next two methods, most of the code is repeated
    # use your fp skillz, player
    def _gen_command_list(self, data):
        header = ['command']
        rows = [header]
        for cmd in data:
            params = data[cmd]['params']
            r = [cmd]
            rows.append([cmd] + ["{0}: ({1})".format(p, params[p]['type']) \
                        for p in params])

        max_len = max([len(r) for r in rows])
        rows[0] += list(range(max_len-1))
        rows = [r + [''] * (max_len - len(r)) for r in rows]
        return rows

    def _gen_execution_list(self, data):
        header = ['Output Block']
        rows = [header]
        for frm in data:
            rows.append([frm] + data[frm])

        max_len = max([len(r) for r in rows])
        rows[0] += list(range(max_len-1))
        rows = [r + [''] * (max_len - len(r)) for r in rows]
        return rows

    def _gen_spec(self, data):
        excl = ['name', 'execution']
        header = [data.get('name'), '']
        rows = [header]
        keys = sorted([k for k in data.keys() if k not in excl])
        for k in keys:
            rows.append([k, data[k]])
        return rows
        
    def _get_table(self, rows):
        header = rows.pop(0)
        tbl = PrettyTable(header)
        for r in rows:
            tbl.add_row(r)
        return tbl
