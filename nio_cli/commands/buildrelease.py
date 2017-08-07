import subprocess
import json

from nio.util.discovery import is_class_discoverable as _is_class_discoverable
from nio.block.base import Block
from niocore.core.loader.discover import Discover

from .base import Base


def is_class_discoverable(_class, default_discoverability=True):
    return _is_class_discoverable(_class, default_discoverability)


class BuildRelease(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._repo = self.options['<repo-name>']
        self._block_releases = {}

    def run(self):
        get_repo_url = "git remote -v"
        git_result = subprocess.check_output(get_repo_url, shell=True)

        blocks = Discover.discover_classes(
            'blocks.{}'.format(self._repo), Block, _is_class_discoverable)
        for block in blocks:
            self._create_block_release(block, git_result.split(' ')[1])

        self._write_repo_release()

    def _write_repo_release(self):
        """write the final release.json file in the repo, containing releases
        for all blocks in the repo.
        """
        file_path = "blocks/{}/release.json".format(self._repo)
        # create file if it does not exist with 'w+' mode
        with open(file_path, "w+") as release_file:
            json.dump(self._block_releases, release_file)

    def _create_block_release(self, block_object, url):
        block_name = block_object.name
        block_version = block_object.version
        block_release = {
            "nio/{}".format(block_name): {
                "language": "Python",
                "version": block_version,
                "reference": url + "@v{}".format(block_version)
            }
        }
        self._block_releases.update(block_release)
