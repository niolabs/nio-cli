"""
nio

Usage:
  nio new <project-name>
  nio server [(--silent | -s)]
  nio [options] add <block-repo>...
  nio [options] (list | ls) services [<service-name> [--cmd | --exec]]
  nio [options] (list | ls) blocks [<block-name> [--cmd]]
  nio [options] (command | co) <command-name> <service-name> [<block-name>] [--args=<args>]
  nio [options] (confg | cfg) services <service-name>
  nio [options] (config | cfg) blocks <block-name>
  nio [options] update <block-type>
  nio [options] (build | ln) <source-block-name>... [<sink-block-name>]
  nio [options] shutdown
  nio -h | --help
  nio --version

Options:
  -p PORT --port=PORT               Specify n.io port.
  -i IP --ip=IP                     Specify n.io ip address.
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  nio new my_project
  nio add util
  nio ls services
  nio co start Service

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/nioinnovation/nio-cli
"""


from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION
from . import commands


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION, options_first=True)
    for k, v in options.items():
        if v and hasattr(commands, k):
            module = getattr(commands, k)
            members = getmembers(module, isclass)
            command = [command[1] for command in members if command[0] != 'Base'][0]
            command(options).run()
