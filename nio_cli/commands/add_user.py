from nio_cli.utils import set_user
from .base import Base


class AddUser(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._project_name = self.options['--project']
        self._username = self.options['<username>']
        self._password = self.options['<password>']

    def run(self):
        set_user(self._project_name, self._username, self._password)