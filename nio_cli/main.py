import sys
import os
from os.path import expanduser, isfile
from argparse import ArgumentParser
from nio_cli.actions import ListAction, CommandAction,\
    ConfigAction, BuildAction, UpdateAction, ServerAction
from nio_cli.util import argument, creds, NIOClient
from nio_cli.nio_add_blocks.main import AddBlocksAction, AddProjectAction, \
    PullBlocksAction

# TODO:
### Protect some of the json ser/deser.

def _nio_instance_configure(args):
    # TODO: replace with pynio
    # initialize the NIOClient
    host = args.ip or os.environ.get('NIOHOST') or 'localhost'
    port = args.port or os.environ.get('NIOPORT') or 8181
    creds = (args.basicauth[0], args.basicauth[1])
    NIOClient.initialize(host, port, creds)

def _nio_instance_main():

    argparser = ArgumentParser(
        description=('''Interact with a running NIO instance. '''
                     '''Requires the v1.x.x API.''')
    )

    # path to nio-instance config file
    argparser.add_argument('-i', '--ip', default=None)
    argparser.add_argument('-p', '--port', default=None)
    argparser.add_argument('-b', '--basicauth', nargs=2,
                           default=['Admin', 'Admin'])

    subparsers = argparser.add_subparsers(help='sub-command help')

    # subcommand for listing blocks, services
    server_parser = subparsers.add_parser('server')
    server_parser.set_defaults(action=ServerAction)
    server_parser.add_argument('-e', '--exec', default='run_nio')
    server_parser.add_argument('-bg', '--background', action='store_true')

    list_parser = subparsers.add_parser('list', aliases=['ls'])
    list_parser.set_defaults(action=ListAction)
    list_parser.add_argument('resource', type=str)
    list_parser.add_argument('names', nargs='*', default=[''])
    list_parser.add_argument('--cmd', action='store_true')
    list_parser.add_argument('--exec', action='store_true')
    list_parser.add_argument('--filter', type=argument, nargs='*')

    cmd_parser = subparsers.add_parser('command', aliases=['co'])
    cmd_parser.set_defaults(action=CommandAction)
    cmd_parser.add_argument('command', type=str)
    cmd_parser.add_argument('service', type=str, nargs='?', default=None)
    cmd_parser.add_argument('block', nargs='?', default='')
    cmd_parser.add_argument('--auto', '-a', action='store_true')
    cmd_parser.add_argument('--args', type=argument, nargs='*', default=[])

    config_parser = subparsers.add_parser('config', aliases=['cfg'])
    config_parser.set_defaults(action=ConfigAction)
    config_parser.add_argument('resource', type=str)
    config_parser.add_argument('name')

    build_parser = subparsers.add_parser('build', aliases=['ln'])
    build_parser.set_defaults(action=BuildAction)
    build_parser.add_argument('-rm', action='store_true')
    build_parser.add_argument('name', type=str)
    build_parser.add_argument('froms', nargs='*', default=[])
    build_parser.add_argument('to')

    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(action=UpdateAction)
    update_parser.add_argument('block_types', type=str, nargs='+')

    # Add Blocks from GitHub
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(action=AddBlocksAction)
    add_parser.add_argument('-f', '--init', default='')
    add_parser.add_argument('repos', type=str, nargs='*')
    add_parser.add_argument('-u', '--update', action='store_true')
    add_parser.add_argument('--https', action='store_true')

    # Create a new nio project from project template on GitHub
    new_parser = subparsers.add_parser('new')
    new_parser.set_defaults(action=AddProjectAction)
    new_parser.add_argument('project_name', default='project_template')
    new_parser.add_argument('--https', action='store_true')

    # Pull blocks from GitHub
    pull_parser = subparsers.add_parser('pull')
    pull_parser.set_defaults(action=PullBlocksAction)
    pull_parser.add_argument('--nc', action="store_true",
        help="Do not do any 'git checkout' during update")
    pull_parser.add_argument('blocks', type=str, nargs='*')

    args = argparser.parse_args()

    # initialization
    _nio_instance_configure(args)

    action = args.action(args)
    try:
        action.perform()
    except Exception as e:
        print("Error while executing nio action {0}".format(
            type(action).__name__), file=sys.stderr)
        print(type(e).__name__, str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    status = _nio_instance_main()
    sys.exit(0)
