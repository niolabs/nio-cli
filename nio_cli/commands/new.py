import subprocess

from .base import Base


class New(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._name = self.options['<project-name>']

    def run(self):
        clone = "git clone git@github.com:{}/{}.git {}"
        subprocess.call(
            clone.format('nioinnovation', 'project_template', self._name),
            shell=True)
