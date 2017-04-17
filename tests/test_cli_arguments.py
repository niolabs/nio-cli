import unittest
from docopt import docopt, DocoptExit
import nio_cli.cli as cli


doc = cli.__doc__


class TestCLIArguments(unittest.TestCase):

    def test_valid_new_command(self):
        """Command 'new' needs a project-name"""
        args = docopt(doc, ['new', 'project-name'])
        self.assertEqual(args['<project-name>'], 'project-name')

    def test_new_command_with_no_project_name(self):
        """Command 'new' fails with no project-name"""
        with self.assertRaises(DocoptExit):
            docopt(doc, ['new'])
