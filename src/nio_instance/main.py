import sys
from argparse import ArgumentParser
from actions import ListAction, CommandAction, ConfigAction, BuildAction
from util import argument, edge, creds, NIOClient

# TODO: 
### Configuration by file.
### Protect some of the json ser/deser.

        
def nio_instance_main():
    
    argparser = ArgumentParser(
        description=('''Interact with a running NIO instance. '''
                     '''Requires the v1.x.x API.''')
    )

    argparser.add_argument('--host', default='localhost')
    argparser.add_argument('-p', '--port', default='8181')
    argparser.add_argument('-u', '--user', type=creds, default='Admin:Admin')

    subparsers = argparser.add_subparsers(help='sub-command help')

    # subcommand for listing blocks, services
    list_parser = subparsers.add_parser('list', aliases=['ls'])
    list_parser.set_defaults(action=ListAction)
    list_parser.add_argument('resource', type=str)
    list_parser.add_argument('names', nargs='*', default=[''])
    list_parser.add_argument('--cmd', action='store_true')

    cmd_parser = subparsers.add_parser('command', aliases=['co'])
    cmd_parser.set_defaults(action=CommandAction)
    cmd_parser.add_argument('command', type=str)
    cmd_parser.add_argument('service', type=str)
    cmd_parser.add_argument('block', nargs='?', default='')
    cmd_parser.add_argument('--interactive', '-i', action='store_true')
    cmd_parser.add_argument('--args', type=argument, nargs='*', default=[])

    config_parser = subparsers.add_parser('config', aliases=['cfg'])
    config_parser.set_defaults(action=ConfigAction)
    config_parser.add_argument('resource', type=str)
    config_parser.add_argument('name')
    
    build_parser = subparsers.add_parser('build', aliases=['ln'])
    build_parser.set_defaults(action=BuildAction)
    build_parser.add_argument('name', type=str)
    if sys.stdin.isatty():
        build_parser.set_defaults(interactive=True)
    build_parser.add_argument('edges', nargs='*', type=edge, default=[])
    build_parser.add_argument('-rm', action='store_true')

    args = argparser.parse_args()

    # configure the API client
    NIOClient.initialize(args.host, args.port, args.user)

    action = args.action(args)
    try:
        action.perform()
    except Exception as e:
        from traceback import format_exc
        print(format_exc())
        print("Error while executing nio action {0}".format(
            type(action).__name__), file=sys.stderr)
        print(type(e).__name__, e, file=sys.stderr)

if __name__ == '__main__':
    nio_instance_main()
    sys.exit(0)
