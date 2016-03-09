import unittest
from unittest.mock import patch
from nio_cli.commands import New as command
from nio_cli.commands.base import Base


class TestCommandNew(unittest.TestCase):

    def test_new_run(self):
        """The 'new' command clones down the project template"""
        with patch('nio_cli.commands.new.subprocess.call') as call:
            self._run_command_with_options({
                '<project-name>': 'project-name'
            })
            self.assertEqual(
                call.call_args[0][0],
                'git clone git@github.com:nioinnovation/project_template.git'
                ' project-name')

    def _run_command_with_options(self, options):
        options['--ip'] = '0.0.0.0'
        options['--port'] = 8181
        command(options).run()
