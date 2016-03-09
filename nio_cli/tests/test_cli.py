import unittest
from unittest.mock import patch
import nio_cli.cli as cli
from nio_cli.commands.base import Base


class TestCLI(unittest.TestCase):

    def test_run(self):
        """The specified command should be 'run'"""
        with patch('nio_cli.cli.docopt') as docopt:
            docopt.return_value = {
                '--ip': '0.0.0.0',
                '--port': '8181',
                'new': True,
                '<project-name>': 'project-name',
            }
            with patch('nio_cli.commands.new.New.run') as run:
                cli.main()
                run.assert_called_once_with()

    def _arguments(self):
        return {
            '--args': None,
            '--cmd': False,
            '--daemon': False,
            '--exec': False,
            '--help': False,
            '--ip': '0.0.0.0',
            '--port': '8181',
            '--upgrade': False,
            '--version': False,
            '-d': False,
            '-u': False,
            '<block-repo>': [],
            '<block-name>': None,
            '<block-type>': None,
            '<command-name>': None,
            '<project-name>': None,
            '<service-name>': None,
            '<sink-block-name>': None,
            '<source-block-name>': [],
            'add': False,
            'blocks': False,
            'build': False,
            'cfg': False,
            'co': False,
            'command': False,
            'confg': False,
            'config': False,
            'list': False,
            'ln': False,
            'ls': False,
            'new': False,
            'server': False,
            'services': False,
            'shutdown': False,
            'update': False,
        }
