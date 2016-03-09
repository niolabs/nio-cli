"""The base command."""


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self._base_url = "http://{}:{}/".format(self.options['--ip'],
                                                self.options['--port'])

    def run(self):
        print('Running base')
        raise NotImplementedError(
            'You must implement the run() method yourself!')
