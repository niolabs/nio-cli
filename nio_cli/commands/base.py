import requests


class Base(object):

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self._base_url = "http://{}:{}/{{}}".format(self.options['--ip'],
                                                    self.options['--port'])
        # default to Admin/Admin
        self._auth = ('Admin', 'Admin')

    def run(self):
        raise NotImplementedError('Implement run() in the command.')

    def get(self, *args, **kwargs):
        return self._execute_request(
            requests.get, *args, auth=self._get_credentials(), **kwargs)

    def post(self, *args, **kwargs):
        return self._execute_request(
            requests.post, *args, auth=self._get_credentials(), **kwargs)

    @staticmethod
    def _execute_request(fn, *args, **kwargs):
        response = fn(*args, **kwargs)
        if response.status_code >= 400:
            msg = "Client error, status: {}, message: {}".format(
                response.status_code, response.reason)
            print(msg)
            raise RuntimeError(msg)

        return response

    def _get_credentials(self):
        # allow to override last credentials set
        (username, password) = self._auth

        if "<username>" in self.options and self.options["<username>"]:
            username = self.options.get("<username>")
        else:
            username = self._gather_input('Username ({}): '.format(username),
                                          username)
        if username:
            if "<password>" in self.options and self.options["<password>"]:
                password = self.options.get("<password>")
            else:
                password = \
                    self._gather_input('Password ({}): '.format(password),
                                       password)
        else:
            # user when asked for username pressed enter or it came in empty
            # from command line ==> use cached credentials
            pass

        # cache last credentials
        self._auth = (username, password)
        return self._auth

    @staticmethod
    def _gather_input(message, default=""):
        user_input = input(message)
        if user_input:
            return user_input
        else:
            return default
