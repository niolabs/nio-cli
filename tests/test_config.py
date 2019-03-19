import unittest
from unittest.mock import mock_open, patch, ANY, call

from nio_cli.utils import config_project
from nio_cli.commands.config import Config


class TestConfig(unittest.TestCase):

    def _run_config(self, isfile=True):
        options = {
            '--ip': None,
            '--port': None,
            '--username': 'Admin',
            '--password': 'Admin',
            '--project': '.'
        }
        with patch('builtins.print') as self.mock_print, \
                patch(Config.__module__ + '.config_project') as self.mock_conf:
            Config(options).run()

    def test_run_project(self):
        self._run_config()
        self.assertEqual(self.mock_conf.call_count, 1)


class TestConfigProject(unittest.TestCase):

    def _run_config_project(self, isfile=True, kwargs={}):
        # Thank you, Martijn Pieters
        #https://stackoverflow.com/questions/24779893/customizing-unittest-mock-mock-open-for-iteration
        # define contents of a fresh nio.conf
        read_data = '\n'.join([
            'PK_HOST=',
            'WS_HOST=',
            'PK_TOKEN=',
            'NIOHOST=',
            'NIOPORT=',
            'et cetera',
            'SSL_CERTIFICATE=',
            'SSL_PRIVATE_KEY=',
            '',  # end with a newline
        ])
        m = mock_open(read_data=read_data)
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        with patch('builtins.open', m) as self.mock_open, \
                patch('builtins.print') as self.mock_print, \
                patch(config_project.__module__ + '.os') as self.mock_os, \
                patch(config_project.__module__ + '.move') as self.mock_move, \
                patch(config_project.__module__ + '.config_ssl') as \
                    self.mock_ssl, \
                patch(config_project.__module__ + '.tempfile') as \
                    mock_tempfile:
            self.mock_ssl.return_value = ('path/to/cert', 'path/to/key')
            self.mock_tempfile = mock_tempfile.NamedTemporaryFile().__enter__()
            self.mock_os.path.isfile.return_value = isfile
            config_project(**kwargs)

    def test_config_project(self):
        self._run_config_project()

        self.assertEqual(self.mock_open.call_count, 1)
        self.assertEqual(self.mock_open.call_args_list[0],
            call('./nio.conf', 'r'))
        self.mock_os.remove.assert_called_once_with('./nio.conf')
        self.mock_move.assert_called_once_with(ANY, ANY)
        self.assertEqual(self.mock_ssl.call_count, 0)

    def test_config_with_pubkeeper_port_ip_flags(self):
        pk_host = 'hostname.pubkeeper.whatever'
        ws_host = pk_host.replace('pubkeeper', 'websocket')
        pk_token = 'token'
        nio_host = '1.2.3.4'
        nio_port = 5678
        self._run_config_project(kwargs={'pubkeeper_hostname': pk_host,
                                         'pubkeeper_token': pk_token,
                                         'niohost': nio_host,
                                         'nioport': nio_port})
        self.assertEqual(self.mock_open.call_count, 1)
        self.assertEqual(
            self.mock_open.call_args_list[0],
            call('./nio.conf', 'r'))
        self.mock_os.remove.assert_called_once_with('./nio.conf')
        self.mock_move.assert_called_once_with(ANY, ANY)
        self.assertEqual(self.mock_tempfile.write.call_count, 8)
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[0],
            call('PK_HOST={}\n'.format(pk_host)))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[1],
            call('WS_HOST={}\n'.format(ws_host)))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[2],
            call('PK_TOKEN={}\n'.format(pk_token)))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[3],
            call('NIOHOST={}\n'.format(nio_host)))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[4],
            call('NIOPORT={}\n'.format(nio_port)))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[5],
            call('et cetera\n'))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[6],
            call('SSL_CERTIFICATE=\n'))
        self.assertEqual(
            self.mock_tempfile.write.call_args_list[7],
            call('SSL_PRIVATE_KEY=\n'))

    def test_config_with_specified_project_location(self):
        path = '/path/to/project'
        conf_location = '{}/nio.conf'.format(path)
        self._run_config_project(kwargs={"name": path})

        self.assertEqual(self.mock_open.call_count, 1)
        self.assertEqual(
            self.mock_open.call_args_list[0],
            call(conf_location, 'r'))
        self.mock_os.remove.assert_called_once_with(conf_location)
        self.mock_move.assert_called_once_with(ANY, ANY)

    def test_config_with_no_nioconf(self):
        self._run_config_project(isfile=False)
        self.mock_print.assert_called_once_with(
            'Command must be run from project root.')
        self.assertEqual(self.mock_open.call_count, 0)

    def test_config_with_ssl(self):
        self._run_config_project(kwargs={"ssl": True})

        self.assertEqual(self.mock_open.call_count, 1)
        self.mock_os.remove.assert_called_once_with('./nio.conf')
        self.mock_move.assert_called_once_with(ANY, ANY)
        self.assertEqual(self.mock_ssl.call_count, 1)

    def _test_open_call_order(self, call_args_list, path='.'):
        open1_call_args = self.mock_open.call_args_list[0]
        self.assertEqual(open1_call_args, call('{}/nio.conf'\
            .format(path), 'r'))
        open2_call_args = self.mock_open.call_args_list[1]
        self.assertEqual(open2_call_args, call('{}/etc/users.json'\
            .format(path), 'r'))
        open3_call_args = self.mock_open.call_args_list[2]
        self.assertEqual(open3_call_args, call('{}/etc/users.json'\
            .format(path), 'w+'))
        open4_call_args = self.mock_open.call_args_list[3]
        self.assertEqual(open4_call_args, call('{}/etc/permissions.json'\
            .format(path), 'r'))
        open5_call_args = self.mock_open.call_args_list[4]
        self.assertEqual(open5_call_args, call('{}/etc/permissions.json'\
            .format(path), 'w+'))
