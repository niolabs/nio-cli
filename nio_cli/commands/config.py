from .base import Base
import requests
import os
import re
import tempfile


def config_project(name='.'):
    env_location = '{}/nio.conf'.format(name)
    if not os.path.isfile(env_location):
        print("Command must be run from project root.")
        return

    pk_host = input('Enter PK Host (optional): ')
    pk_token = input('Enter PK Token (optional): ')
    ws_host = pk_host.replace('pubkeeper', 'websocket')

    with open(env_location, 'r') as nenv,\
     tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        for line in nenv:
            if re.search('^PK_HOST=', line) and pk_host:
                tmp.write('PK_HOST={}\n'.format(pk_host))
            elif re.search('^WS_HOST=', line) and pk_host:
                tmp.write('WS_HOST={}\n'.format(ws_host))
            elif re.search('^PK_TOKEN=', line) and pk_token:
                tmp.write('PK_TOKEN={}\n'.format(pk_token))
            else:
                tmp.write(line)
    os.remove(env_location)
    os.rename(tmp.name, env_location)


class Config(Base):
    """ Get basic nio info """

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._resource = 'services' if self.options.get('services') else \
            'blocks' if self.options.get('blocks') else \
            'project'
        self._resource_name = \
            self.options.get('<service-name>') if self.options.get('services') else \
            self.options.get('<block-name>') if self.options.get('blocks') else \
            ""

    def config_block_or_service(self):
        response = requests.get(
            self._base_url.format(
                '{}/{}'.format(self._resource, self._resource_name)),
            auth=self._auth)
        try:
            config = response.json()
            print(config)
        except Exception as e:
            print(e)

    def run(self):
        if self._resource == 'project':
            config_project()
        else:
            self.config_block_or_service()
