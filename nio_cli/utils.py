import os
import json
from base64 import b64encode
import re
import tempfile

def config_project(name='.', pubkeeper_hostname=None, pubkeeper_token=None,
                   username=None, password=None):
    conf_location = '{}/nio.conf'.format(name)
    if not os.path.isfile(conf_location):
        print("Command must be run from project root.")
        return

    pk_host = input('Enter Pubkeeper hostname (optional): ') \
        if pubkeeper_hostname is None else pubkeeper_hostname
    pk_token = input('Enter Pubkeeper token (optional): ') \
        if pubkeeper_token is None else pubkeeper_token
    ws_host = pk_host.replace('pubkeeper', 'websocket')

    # allow to set a user
    set_user(name, username, password)

    with open(conf_location, 'r') as nconf,\
            tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        for line in nconf:
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

    secure = input('Optional secure instance configuration [y/N]: ')
    if secure.lower() == 'y':
        _config_ssl(name, conf_location)


def _config_ssl(name, conf_location):

    cwd = os.getcwd()

    new_certs = input('Generate a self-signed certificate/key [y/N]: ')

    if new_certs.lower() == 'y':
        try:
            from OpenSSL import crypto
        except Exception as e:
            print('No pyOpenSSL installation detected. Your instance has still '
                  'been configured but no certs were installed. To install '
                  'certificates install pyOpenSSL and re-run "nio config" from '
                  'inside the project directory.')
            return

        # Create a key pair
        kp = crypto.PKey()
        kp.generate_key(crypto.TYPE_RSA, 2048)

        # Create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = input('Enter two-letter country code: ')
        cert.get_subject().ST = input('Enter state: ')
        cert.get_subject().L = input('Enter city: ')
        cert.get_subject().O = input('Enter company/owner: ')
        cert.get_subject().OU = input('Enter user: ')
        cert.get_subject().CN = 'localhost'
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(kp)
        cert.sign(kp, 'sha1')

        open('{}/certificate.pem'.format(name), "wt").write(
            str(crypto.dump_certificate(crypto.FILETYPE_PEM, cert)))
        open('{}/private_key.pem'.format(name), "wt").write(
            str(crypto.dump_privatekey(crypto.FILETYPE_PEM, kp)))

        ssl_cert = '{}/{}/certificate.pem'.format(cwd, name)
        ssl_key = '{}/{}/private_key.pem'.format(cwd, name)

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


def set_user(project_name, username, password):
    # load users
    users_location = '{}/etc/users.json'.format(project_name)
    if os.path.isfile(users_location):
        with open(users_location, 'r') as f:
            users = json.load(f)
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
        _set_permissions(project_name, username)
    else:
        print('Username cannot be empty')

def _set_permissions(project_name, username):
    # Add new user with admin level permission
    permission_location = '{}/etc/permissions.json'.format(project_name)
    if os.path.isfile(permission_location):
        with open(permission_location, 'r') as f:
            permissions = json.load(f)
    else:
        permissions = {}

    print('Adding permissions for user: {}'.format(username))
    permissions[username] = {
        ".*": "rwx"
    }
    # write it back
    with open(permission_location, 'w+') as f:
        json.dump(permissions, f, indent=4, separators=(',', ': '))

def _base64_encode(s, encoding='ISO-8859-1'):
    """Return the native string base64-encoded (as a native string)."""
    if isinstance(s, str):
        b = s.encode(encoding)
    else:
        b = s
    b = b64encode(b)
    return b.decode(encoding)
