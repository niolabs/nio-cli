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

    def _get_table(self, rows):
        align = rows.pop(0)
        header = rows.pop(0)
        tbl = PrettyTable(header)
        for col, a in align:
            tbl.align[col] = a
        for r in rows:
            tbl.add_row(r)
        return tbl
