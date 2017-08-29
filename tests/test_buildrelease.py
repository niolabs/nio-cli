import unittest
from unittest import skipIf

try:
    from nio_cli.commands.buildrelease import BuildRelease
    niocore_installed = True
except:
    niocore_installed = False


class TestCLI(unittest.TestCase):

    @skipIf(not niocore_installed, 'niocore required for buildrelease')
    def test_buildrelease_git_remote_url_parse(self):
        """Support multiple repo url formats from `git remote -v`"""
        buildrelease = BuildRelease({
            '<repo-name>': '', '--ip': '', '--port': '',
        })
        parse = buildrelease.parse_url_from_git_remote_command
        self.assertEqual(
            parse(b"origin git@github.com:nio-blocks/repo.git (fetch)"),
            "git://github.com/nio-blocks/repo.git")
        self.assertEqual(
            parse(b"origin git@github.com:/nio-blocks/repo (fetch)"),
            "git://github.com/nio-blocks/repo.git")
        self.assertEqual(
            parse(b"origin https://github.com/nio-blocks/repo (fetch)"),
            "git://github.com/nio-blocks/repo.git")
        self.assertEqual(
            parse(b"origin https://1.2.3.4/nio-blocks/repo (fetch)"),
            "git://1.2.3.4/nio-blocks/repo.git")
