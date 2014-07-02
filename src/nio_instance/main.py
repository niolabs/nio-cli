import requests
import sys
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

class Consumer(Thread):
    
    def __init__(self, resp_queue):
        super().__init__(target=self.consume, daemon=True)
        self._queue = resp_queue
        self._stop = Event()

    def consume(self):
        while(not self._stop.is_set()):
            rsp = self._queue.get()
            print(rsp.json())

    def stop(self):
        self._stop.set()


def _list_url(args):
    url = LIST_FORMAT.format(args.host, args.port, args.resource, args.name)
    return url

def _list_process_rsp(args, rsp):
    data = rsp.json()
    good_fields = ['name', 'type', 'log_level', 'auto_start', 'sys_metadata', 'mappings']
    if args.name is not None:
        pass
        # do something to show the execution of the particular service
    eg = list(data.values())[0]
    keys = sorted([k for k in eg if k in good_fields])

    if sys.stdout.isatty():
        tbl = PrettyTable(keys)
        for k in data:
            tbl.add_row([data[k].get(j) for j in keys])
        print(tbl)
    else:
        for k in data:
            print(_format_line(data[k], keys))

def _format_line(resource, keys):
        return ' '.join([str(resource[k]) for k in keys])
                  

def _command_url(args):
    url = COMMAND_FORMAT.format(args.host, args.port, args.service, args.block)
    if args.cmd is not None:
        url = '{0}{1}'.format(url, args.cmd)
    elif args.list:
        url = '{0}{1}'.format(url, 'commands')

    return url

def _command_process_rsp(args, rsp):
    print(rsp.json())

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
    list_parser.set_defaults(get_url=_list_url,
                             process_rsp=_list_process_rsp)
    list_parser.add_argument('resource', type=str)
    list_parser.add_argument('--name', default='')

    cmd_parser = subparsers.add_parser('command', aliases=['co'])
    cmd_parser.set_defaults(get_url=_command_url,
                            process_rsp=_command_process_rsp)
    cmd_parser.add_argument('service', type=str)
    cmd_parser.add_argument('block', nargs='?', default='')
    cmd_parser.add_argument('--cmd', type=str)
    cmd_parser.add_argument('--list', action='store_true')

    args = argparser.parse_args()

    url = args.get_url(args)
    try:
        rsp = requests.request('GET', url, auth=('Admin', 'Admin'))
    except Exception as e:
        print(type(e), e, file=sys.stderr)
        sys.exit(1)

    status = rsp.status_code

    if status == 200:
        if rsp.text:
            args.process_rsp(args, rsp)
        else:
            print('`%s`' % rsp.request.url, "was processed successfully")
    else:
        print("NIO request returned status %d" % status, file=sys.stderr)

if __name__ == '__main__':
    nio_instance_main()
    sys.exit(0)
    
