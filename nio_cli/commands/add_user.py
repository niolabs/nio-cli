import os
import json
from base64 import b64encode


from .base import Base


class AddUser(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._project_name = self.options['<project-name>'] or "."
        self._username = self.options['--username']
        self._password = self.options['--password']

    def run(self):
        set_user(self._project_name, self._username, self._password)


def set_user(project_name, username, password):
    # load users
    users_location = '{}/etc/users.json'.format(project_name)
    if os.path.isfile(users_location):
        with open(users_location, 'r') as f:
            users = json.loads(f.read())
    else:
        users = {}

    # add/override this user and password
    username = input('Username: ') if username is None else username
    # if username is valid
    if username:
        password = input('Password: ') if password is None else password
        print('Adding user: {}'.format(username))
        users[username] = {
            "password": _base64_encode(password)
        }
        # write it back
        with open(users_location, 'w+') as f:
            json.dump(users, f, indent=4, separators=(',', ': '))
    else:
        print('Username cannot be empty')


def _base64_encode(s, encoding='ISO-8859-1'):
    """Return the native string base64-encoded (as a native string)."""
    if isinstance(s, str):
        b = s.encode(encoding)
    else:
        b = s
    b = b64encode(b)
    return b.decode(encoding)
