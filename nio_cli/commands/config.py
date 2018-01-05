from .base import Base
import requests
import subprocess
import os


def config_project(name='.'):
    env_location = '{}/nio.env'.format(name)
    if not os.path.isfile(env_location):
        print("Command must be run from project root.")
        return

    pk_host = input('Enter PK Host (optional): ')
    pk_token = input('Enter PK Token (optional): ')
    ws_host = pk_host.replace('pubkeeper', 'websocket')

    pk_host_replace = "s/^PK_HOST:.*/PK_HOST: {}/".format(pk_host)
    pk_token_replace = "s/^PK_TOKEN:.*/PK_TOKEN: {}/".format(pk_token)
    ws_host_replace = "s/^WS_HOST:.*/WS_HOST: {}/".format(ws_host)

    if pk_host:
        subprocess.call(
            'sed -i "" "{}" {}'.format(pk_host_replace, env_location),
            shell=True)
        subprocess.call(
            'sed -i "" "{}" {}'.format(ws_host_replace, env_location),
            shell=True)
    if pk_token:
        subprocess.call(
            'sed -i "" "{}" {}'.format(pk_token_replace, env_location),
            shell=True)



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
