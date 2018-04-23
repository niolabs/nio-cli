import os
import subprocess
import sys

from .base import Base


class Add(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._blocks = self.options['<block-repo>']
        self._upgrade = self.options['--upgrade'] or self.options['-u']

    def run(self):
        # Add block repos as submodules
        for block in self._blocks:
            submodule = "git submodule add git://github.com/{}/{}.git ./{}/{}"
            subprocess.call(
                submodule.format('nio-blocks', block, 'blocks', block),
                shell=True)
        # Initialize all submodules
        subprocess.call("git submodule update --init --recursive", shell=True)
        # Upgrade blocks if requested
        # Note: This needs to happen after `submodule update` or else the repos
        # will go back to the previously committed version of the submodules.
        for block in self._blocks:
            if self._upgrade:
                self._upgrade_block(block)
        # Install block dependencies
        for block in self._blocks:
            block_path = 'blocks/{}'.format(block)
            for root, dirs, files in os.walk(block_path):
                for file_name in files:
                    if file_name == 'requirements.txt':
                        reqs = os.path.join(root, file_name)
                        subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', reqs])

    def _upgrade_block(self, block):
        checkout = "cd ./{}/{} && git checkout {}"
        subprocess.call(checkout.format('blocks', block, 'master'), shell=True)
        update = "cd ./{}/{} && git pull --ff-only --recurse-submodules --all"
        subprocess.call(update.format('blocks', block), shell=True)
