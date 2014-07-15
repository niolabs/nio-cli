import sys
from argparse import ArgumentParser
from actions import ListAction, CommandAction, ConfigAction, LinkAction
from util import argument, link

        
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
    
    link_parser = subparsers.add_parser('link', aliases=['cxn'])
    link_parser.set_defaults(action=LinkAction)
    link_parser.add_argument('name', type=str)
    link_parser.add_argument('links', nargs='*', type=link)
    link_parser.add_argument('-i', action='store_true')
    link_parser.add_argument('-rm', action='store_true')

    args = argparser.parse_args()

    action = args.action(args)
    action.perform()

if __name__ == '__main__':
    nio_instance_main()
    sys.exit(0)


# class NIORequest(Thread):
    
#     def __init__(self, cmd='GET', 
#                  url='https://localhost:8181/nio', 
#                  resp_queue=None):
#         super().__init__(target=self.request, args=(cmd, url))
#         self._queue = resp_queue

#     def request(self, cmd, url):
#         try:
#             rsp = requests.request(cmd, url, auth=('Admin', 'Admin'))
#             self._queue.put(rsp)
#         except Exception as e:
#             print(type(e), e, file=sys.stderr)

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

