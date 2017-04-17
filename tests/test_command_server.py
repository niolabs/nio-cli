import unittest
from unittest.mock import patch
from nio_cli.commands import Server


class TestCommandServer(unittest.TestCase):

    def test_server(self):
        """The 'server' command executes nio binary as a subprocess"""
        with patch('nio_cli.commands.server.subprocess.Popen') as Popen:
            options = {}
            options['--daemon'] = False
            options['-d'] = False
            options['--ip'] = '0.0.0.0'
            options['--port'] = 8181
            Server(options).run()
            self.assertEqual(Popen.call_args[0][0], ['nio_full'])
