import os
import json

from .base import Base


class RemoveUser(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._project_name = self.options['--project']
        self._username = self.options['<username>']

    def run(self):
        remove_user(self._project_name, self._username)


def remove_user(project_name, username):
    # load users
    users_location = '{}/etc/users.json'.format(project_name)
    if os.path.isfile(users_location):
        with open(users_location, 'r') as f:
            users = json.load(f)
    else:
        # No users to remove from
        return

    # remove this user and permissions
    if username in users:
        print('Removing user: {}'.format(username))
        del users[username]
        # write it back
        with open(users_location, 'w+') as f:
            json.dump(users, f, indent=4, separators=(',', ': '))
        _remove_permission(project_name, username)
    else:
        print('User: {} is invalid'.format(username))

def _remove_permission(project_name, username):
    # load users
    permissions_location = '{}/etc/permissions.json'.format(project_name)
    if os.path.isfile(permissions_location):
        with open(permissions_location, 'r') as f:
            permissions = json.load(f)
    else:
        # No users to remove from
        return

    # remove permissions
    if username in permissions:
        print('Removing permissions for user: {}'.format(username))
        del permissions[username]
        # write it back
        with open(permissions_location, 'w+') as f:
            json.dump(permissions, f, indent=4, separators=(',', ': '))
    else:
        print('User permissions for {} is invalid'.format(username))
