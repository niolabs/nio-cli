import subprocess

from .base import Base


class New(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._name = self.options['<project-name>']
        self._template = self.options['<template>']

    def run(self):
        repo = 'git://github.com/niolabs/project_template.git'
        if self._template:
            if 'github.com' in self._template:
                repo = self._template
            else:
                repo = 'git://github.com/niolabs/{}.git'.format(self._template)

        clone = "git clone --depth=1 {} {}".format(repo, self._name)
        submodule_update = (
            'cd ./{} '
            '&& git submodule update --init --recursive'
        ).format(self._name)
        reinit_repo = (
            'cd ./{} '
            '&& git remote remove origin '
            '&& git commit --amend --reset-author -m "Initial commit"'
        ).format(self._name)
        subprocess.call(clone, shell=True)
        subprocess.call(submodule_update, shell=True)
        subprocess.call(reinit_repo, shell=True)
