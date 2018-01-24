from .base import Base
import requests
import os
import re
import tempfile


def config_project(name='.'):
    env_location = '{}/nio.env'.format(name)
    if not os.path.isfile(env_location):
        print("Command must be run from project root.")
        return

    pk_host = input('Enter PK Host (optional): ')
    pk_token = input('Enter PK Token (optional): ')
    ws_host = pk_host.replace('pubkeeper', 'websocket')

    nenv = open(env_location, 'r')
    tmp = tempfile.NamedTemporaryFile(mode='w', delete=False)
    for line in nenv:
        if re.search('PK_HOST:', line) and pk_host:
            tmp.write(re.sub('PK_HOST:.*',
                'PK_HOST: {}'.format(pk_host), line))
        elif re.search('WS_HOST:', line) and pk_host:
            tmp.write(re.sub('WS_HOST:.*',
                'WS_HOST: {}'.format(ws_host), line))
        elif re.search('PK_TOKEN:', line) and pk_token:
            tmp.write(re.sub('PK_TOKEN:.*',
                'PK_TOKEN: {}'.format(pk_token), line))
        else:
            tmp.write(line)
    nenv.close()
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
