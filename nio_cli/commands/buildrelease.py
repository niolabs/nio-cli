import subprocess
import json
import sys
import os
import re

from nio.util.discovery import is_class_discoverable as _is_class_discoverable
from nio.block.base import Base as BaseBlock
try:
    from niocore.core.loader.discover import Discover
except:
    # prevent `main` from failing on `from nio_cli import commands` if
    # `niocore` not available
    pass

from .base import Base


def is_class_discoverable(_class, default_discoverability=True):
    return _is_class_discoverable(_class, default_discoverability)


class BuildRelease(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._repo = self.options['<repo-name>']
        self._block_releases = {}

    def run(self):
        get_repo_url = "cd blocks/{} && git remote -v".format(self._repo)
        git_remote = subprocess.check_output(get_repo_url, shell=True)
        repo_url = self.parse_url_from_git_remote_command(git_remote)

        sys.path.insert(0, os.getcwd())
        blocks = Discover.discover_classes(
            'blocks.{}'.format(self._repo), BaseBlock, is_class_discoverable)
        for block in blocks:
            self._create_block_release(block, repo_url)

        self._write_repo_release()

    def parse_url_from_git_remote_command(self, git_remote):
        repo_url = git_remote.split()[1].decode()
        # Support multiple repo url formats like:
        #   git@github.com:nio-blocks/repo.git
        #   git@github.com:/nio-blocks/repo
        #   https://github.com/nio-blocks/repo
        git_remote_match = r"(git@|https?:\/\/)([^:\/]*)[:\/]+(.*)\/(\w*)"
        parsed_repo_url = re.search(git_remote_match, repo_url)
        git_host = parsed_repo_url.group(2)
        git_org = parsed_repo_url.group(3)
        git_repo = parsed_repo_url.group(4)
        new_git_url = "git://{}/{}/{}.git".format(git_host, git_org, git_repo)
        return new_git_url

    def _write_repo_release(self):
        """write the final release.json file in the repo, containing releases
        for all blocks in the repo.
        """
        file_path = "blocks/{}/release.json".format(self._repo)
        # create file if it does not exist with 'w+' mode
        with open(file_path, "w+") as release_file:
            # sort keys alphabetically
            json.dump(self._block_releases, release_file, indent=2,
                      sort_keys=True)

    def _create_block_release(self, block_object, git_url):
        block_name = block_object.__name__
        block_version = block_object.get_description()["properties"]["version"]["default"]
        block_release = {
            "nio/{}".format(block_name): {
                "language": "Python",
                "version": block_version,
                "url": git_url,
            }
        }
        self._block_releases.update(block_release)
