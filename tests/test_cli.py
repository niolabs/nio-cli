import unittest
from unittest.mock import mock_open, patch, ANY
from docopt import docopt, DocoptExit
import responses
import nio_cli.cli as cli


class TestCLI(unittest.TestCase):

    def parse_args(self, command):
        return docopt(cli.__doc__, command.split(' '))

    def test_new_arguments(self):
        """'new' requires a project-name"""
        args = self.parse_args('new project')
        self.assertEqual(args['<project-name>'], 'project')
        with self.assertRaises(DocoptExit):
            self.parse_args('new')

    def test_server_arguments(self):
        """'server' has optional daemon flags"""
        args = self.parse_args('server')
        self.assertEqual(args['--daemon'], False)
        self.assertEqual(args['-d'], False)
        args = self.parse_args('server --daemon')
        self.assertEqual(args['--daemon'], True)
        self.assertEqual(args['-d'], False)
        args = self.parse_args('server -d')
        self.assertEqual(args['--daemon'], False)
        self.assertEqual(args['-d'], True)

    def test_new_command(self):
        """Clone the project template from GitHub"""
        with patch('nio_cli.commands.new.subprocess.call') as call:
            self._main('new', **{'<project-name>': 'project'})
            self.assertEqual(call.call_args[0][0], (
                'git clone '
                'git@github.com:nioinnovation/project_template.git project'
            ))

    def test_server_command(self):
        """Execute nio_run as a subprocess"""
        with patch('nio_cli.commands.server.subprocess.Popen') as Popen:
            self._main('server')
            self.assertEqual(Popen.call_args[0][0], ['nio_run'])

    def test_add_command(self):
        """Clone specified blocks as submodules"""
        with patch('nio_cli.commands.add.subprocess.call') as call:
            self._main('add', **{'<block-repo>': ['block1']})
            self.assertEqual(call.call_args_list[0][0][0], (
                'git submodule add git@github.com:nio-blocks/block1.git '
                './blocks/block1'
            ))
            self.assertEqual(call.call_args_list[1][0][0], (
                'git submodule update --init --recursive'
            ))

    @responses.activate
    def test_list_command(self):
        """List blocks or services from the rest api"""
        service_response=[{'api': 'response'}, {'another': 'service'}]
        responses.add(responses.GET,
                      'http://127.0.0.1:8181/services',
                      json=service_response)
        with patch('builtins.print') as print:
            self._main('list', services=True)
            self.assertEqual(len(responses.calls), 1)
            self.assertEqual(print.call_count, len(service_response))
            for index, service in enumerate(service_response):
                self.assertDictEqual(
                    print.call_args_list[index][0][0], service)

    @responses.activate
    def test_shutdown_command(self):
        """Shutdown nio through the rest api"""
        responses.add(responses.GET, 'http://127.0.0.1:8181/shutdown')
        self._main('shutdown')
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_command_command(self):
        """Command a nio block through the rest api"""
        responses.add(responses.POST,
                      'http://127.0.0.1:8181/services/service/block/command')
        self._main('command', **{
            '<command-name>': 'command',
            '<service-name>': 'service',
            '<block-name>': 'block',
        })
        self.assertEqual(len(responses.calls), 1)

    def test_buildspec_command(self):
        """Create spec.json file from block class"""

        from nio.block.base import Block
        from nio.properties import StringProperty, VersionProperty
        #from nio.commands import

        class SampleBlock1(Block):
            version = VersionProperty('0.1.0')
            str_prop = StringProperty(
                title='String Prop',
                default='default string',
            )
            another = StringProperty(
                title='Another Prop',
            )

        class SampleBlock2(Block):
            pass

        discover_path = 'nio_cli.commands.buildspec.Discover.discover_classes'
        json_dump_path = 'nio_cli.commands.buildspec.json.dump'
        with patch(discover_path) as discover_classes, \
                patch('builtins.open', mock_open()) as mock_file, \
                patch(json_dump_path) as mock_json_dump:
            discover_classes.return_value = [SampleBlock1, SampleBlock2]
            self._main('buildspec', **{'<repo-name>': 'myblocks'})
            discover_classes.assert_called_once_with(
                'blocks.myblocks', ANY, ANY)
            mock_file.assert_called_once_with('blocks/myblocks/spec.json', 'w')
            mock_json_dump.assert_called_once_with(ANY, mock_file())
            self.assertDictEqual(mock_json_dump.call_args[0][0], {
                "nio/SampleBlock1": {
                    "Version": "0.1.0",
                    "Properties": {
                        "String Prop": {
                            "default": "default string",
                        },
                        "Another Prop": {},
                    },
                },
                "nio/SampleBlock2": {
                    "Version": "0.0.0",
                    "Properties": {
                    },
                },
            })

    def _main(self, command, ip='127.0.0.1', port='8181', **kwargs):
        args = {
            '--ip': ip,
            '--port': port,
            '--daemon': False,
            '-d': False,
            '--upgrade': False,
            '-u': False,
        }
        args[command] = True
        for k, v in kwargs.items():
            args[k] = v
        with patch('nio_cli.cli.docopt') as docopt:
            docopt.return_value = args
            cli.main()
