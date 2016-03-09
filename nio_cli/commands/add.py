import os
import subprocess

import pip

from .base import Base


class Add(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._blocks = self.options['<block-repo>']

    def run(self):
        submodule = "git submodule add git@github.com:{}/{}.git ./{}/{}"
        for block in self._blocks:
            # Add block repo as submodule
            subprocess.call(
                submodule.format('nio-blocks', block, 'blocks', block),
                shell=True)
            # Initialize all submodules
            subprocess.call(
                "git submodule update --init --recursive",
                shell=True)
            # Install block dependencies
            block_path = 'blocks/{}'.format(block)
            for root, dirs, files in os.walk(block_path):
                for file_name in files:
                    if file_name == 'requirements.txt':
                        reqs = os.path.join(root, file_name)
                        pip.main(['install', '-r', reqs])
