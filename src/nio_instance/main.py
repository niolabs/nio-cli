import requests
import sys
import json
from argparse import ArgumentParser
from threading import Thread, Event
from queue import Queue
from prettytable import PrettyTable

LIST_FORMAT = "http://{0}:{1}/{2}/{3}"
COMMAND_FORMAT = "http://{0}:{1}/services/{2}/{3}/"

class NIORequest(Thread):
    
    def __init__(self, cmd='GET', 
                 url='https://localhost:8181/nio', 
                 resp_queue=None):
        super().__init__(target=self.request, args=(cmd, url))
        self._queue = resp_queue

    def request(self, cmd, url):
        try:
            rsp = requests.request(cmd, url, auth=('Admin', 'Admin'))
            self._queue.put(rsp)
        except Exception as e:
            print(type(e), e, file=sys.stderr)

# class Consumer(Thread):
    
#     def __init__(self, resp_queue):
#         super().__init__(target=self.consume, daemon=True)
#         self._queue = resp_queue
#         self._stop = Event()

#     def consume(self):
#         while(not self._stop.is_set()):
#             rsp = self._queue.get()
#             print(rsp.json())

#     def stop(self):
#         self._stop.set()

class Action(object):
    def __init__(self, args, cmd):
        self.args = args
        self.urls = self._create_url()
        self.cmd = cmd
        self.auth = ('Admin', 'Admin')

    def make_request(self, data=None):
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

    def _gen_command_list(self, data):
        header = ['command']
        rows = [header]
        for cmd in data:
            params = data[cmd]['params']
            r = [cmd]
            rows.append([cmd] + ["{0}: ({1})".format(p, params[p]['type']) \
                        for p in params])

        max_len = max([len(r) for r in rows])
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

class CommandAction(Action):

    def __init__(self, args):
        super().__init__(args, 'POST')
        self.fields = ['title', 'params']

    def _create_url(self):
        url = COMMAND_FORMAT.format(self.args.host, self.args.port,
                                    self.args.service, self.args.block)

        url += self.args.command
        return [url]

    def make_request(self):
        data = {}
        for a in self.args.args:
            param, arg = a
            data[param] = arg

        super().make_request(json.dumps(data))

    def _process_rsp(self, rsp):
        data = rsp.json()
        print(data)

class ConfigAction(Action):

    def __init__(self, args):
        super().__init__(args, 'PUT')

    def _create_url(self):
        return [LIST_FORMAT.format(self.args.host, self.args.port,
                                   self.args.resource, self.args.name)]

    def _create_types_url(self):
        return LIST_FORMAT.format(self.args.host, self.args.port,
                                  "%s_types" % self.args.resource, '')
        
    def make_request(self):
        excl = ['name', 'sys_metadata']
        data = {}

        # TODO: boldly unsafe
        block = requests.get(self.urls[0], auth=self.auth).json()
        block_type = block['type']
        type_url = self._create_types_url()
        all_blocks = requests.get(type_url, auth=self.auth).json()
        block_props = all_blocks[block_type].get('properties', {})
        for prop in [b for b in block_props if b not in excl]:
            detail = block_props[prop]
            if not detail.get('readonly', False):
                val = input("%s (%s): " % (prop, detail['type']))
                if detail['type'] == 'int':
                    val = int(val)
                data[prop] = val or block[prop]

        super().make_request(json.dumps(data))
        
        pass


def argument(s):
    try:
        terms = s.split('=')
        try:
            terms[1] = int(terms[1])
        except:
            pass
        return terms
    except:
        raise ArgumentTypeError("Command arguments must be of form 'foo=bar'")
        
        
def nio_instance_main():
    
    argparser = ArgumentParser(
        description=('''Interact with a running NIO instance. '''
                     '''Requires the v1.x.x API.''')
    )

    argparser.add_argument('--host', default='localhost')
    argparser.add_argument('-p', '--port', default='8181')

    subparsers = argparser.add_subparsers(help='sub-command help')

    # subcommand for listing blocks, services
    list_parser = subparsers.add_parser('list', aliases=['ls'])
    list_parser.set_defaults(action=ListAction)
    list_parser.add_argument('resource', type=str)
    list_parser.add_argument('name', nargs='*', default='')
    list_parser.add_argument('--cmd', action='store_true')

    cmd_parser = subparsers.add_parser('command', aliases=['co'])
    cmd_parser.set_defaults(action=CommandAction)
    cmd_parser.add_argument('command', type=str)
    cmd_parser.add_argument('service', type=str)
    cmd_parser.add_argument('block', nargs='?', default='')
    cmd_parser.add_argument('--args', type=argument, nargs='*', default=[])

    config_parser = subparsers.add_parser('config', aliases=['cfg'])
    config_parser.set_defaults(action=ConfigAction)
    config_parser.add_argument('resource', type=str)
    config_parser.add_argument('name')

    args = argparser.parse_args()

    action = args.action(args)
    action.make_request()

if __name__ == '__main__':
    nio_instance_main()
    sys.exit(0)
