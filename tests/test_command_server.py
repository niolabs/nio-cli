import unittest
from unittest.mock import patch
from nio_cli.commands import Server


class TestCommandServer(unittest.TestCase):

    def test_server_run(self):
        """The 'server' command executes nio binary as a subprocess"""
        with patch('nio_cli.commands.server.subprocess.Popen') as Popen:
            options = {}
            options['--daemon'] = False
            options['-d'] = False
            options['--ip'] = '127.0.0.1'
            options['--port'] = 8181
            options['--run'] = True
            Server(options).run()
            self.assertEqual(Popen.call_args[0][0], ['nio_run'])

    def test_server_full(self):
        """The 'server' command executes nio binary as a subprocess"""
        with patch('nio_cli.commands.server.subprocess.Popen') as Popen:
            options = {}
            options['--daemon'] = False
            options['-d'] = False
            options['--ip'] = '127.0.0.1'
            options['--port'] = 8181
            options['--full'] = True
            Server(options).run()
            self.assertEqual(Popen.call_args[0][0], ['nio_full'])