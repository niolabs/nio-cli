import os
import json


from .base import Base


class RemoveUser(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._project_name = self.options['<project-name>'] or "."
        self._username = self.options['--username']

    def run(self):
        remove_user(self._project_name, self._username)


def remove_user(project_name, username):
    # load users
    users_location = '{}/etc/users.json'.format(project_name)
    if os.path.isfile(users_location):
        with open(users_location, 'r') as f:
            users = json.loads(f.read())
    else:
        users = {}

    # add/override this user and password
    username = input('Username: ') if username is None else username
    if username:
        if username in users:
            print('Removing user: {}'.format(username))
            del users[username]
            # write it back
            with open(users_location, 'w+') as f:
                json.dump(users, f, indent=4, separators=(',', ': '))
        else:
            print('User: {} is invalid'.format(username))
    else:
        print('Username cannot be empty')
