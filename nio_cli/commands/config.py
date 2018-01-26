from .base import Base
import requests
import os
import re
import tempfile
import subprocess


def config_project(name='.'):
    conf_location = '{}/nio.conf'.format(name)
    if not os.path.isfile(conf_location):
        print("Command must be run from project root.")
        return

    pk_host = input('Enter PK Host (optional): ')
    pk_token = input('Enter PK Token (optional): ')
    ws_host = pk_host.replace('pubkeeper', 'websocket')

    with open(conf_location, 'r') as nenv,\
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
        os.remove(conf_location)
        os.rename(tmp.name, conf_location)
    secure = input('Optional secure instance configuration [Y/N]: ')
    if secure.lower() == 'y':
        config_ssl(name, conf_location)

# Assumes the user has OpenSSL already installed


def config_ssl(name, conf_location):
    ssl_cert = ''
    ssl_key = ''

    new_certs = input('Generate a self-signed certificate/key [Y/N]: ')

    if (new_certs.lower() == 'y'):
        subprocess.call('mkdir ssl &&  cd ssl', shell=True)
        country = input('Enter two-letter country code: ')
        state = input('Enter two-letter state code: ')
        city = input('Enter city: ')
        org = input('Enter name of organization: ')
        owner = input('Enter name of owner: ')
        user = input('Enter name of user: ')

        gen_cert = ('openssl req -newkey rsa:2048 -nodes -keyout key.pem \
                    -x509 -days 365 -out certificate.pem -subj \
                    "/C={}/ST={}/L={}/O={}/OU=<{}/CN=localhost"').format(
            country, state, city, org, owner, user)
        subprocess.call(gen_cert, shell=True)
        subprocess.call(
            'openssl pkcs12 -inkey key.pem -in certificate.pem -export -out certificate.p12 -passout pass:', shell=True)
        subprocess.call(
            'openssl pkcs12 -in certificate.p12 -noout -info -passin pass:', shell=True)

        ssl_cert = os.getcwd() + '/certificate.pem'
        ssl_key = os.getcwd() + '/key.pem'

    else:
        ssl_cert = input('Enter SSL certificate file location: ')
        ssl_key = input('Enter SSL private key file location: ')

    with open(conf_location, 'r') as nconf,\
            tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        for line in nconf:
            if re.search('^ssl_certificate:', line) and ssl_cert:
                tmp.write('ssl_certificate: {}\n'.format(ssl_cert))
            elif re.search('^ssl_private_key:', line) and ssl_key:
                tmp.write('ssl_private_key: {}\n'.format(ssl_key))
            else:
                tmp.write(line)
        os.remove(conf_location)
        os.rename(tmp.name, conf_location)


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
