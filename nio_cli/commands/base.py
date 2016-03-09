class Base(object):

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self._base_url = "http://{}:{}/".format(self.options['--ip'],
                                                self.options['--port'])

    def run(self):
        raise NotImplementedError('Implement run() in the command.')
