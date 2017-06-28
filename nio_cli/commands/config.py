from .base import Base
import requests

class Config(Base):
    """ Get basic nio info """

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._resource = 'services' if self.options['services'] else 'blocks'
        self._resource_name = \
            self.options['<service-name>'] if self.options['services'] else \
            self.options['<block-name>'] if self.options['blocks'] else \
            ""

    def run(self):
        response = requests.get(
            self._base_url.format(
                '{}/{}'.format(self._resource, self._resource_name)),
            auth=self._auth)
        try:
            config = response.json()
            print(config)
        except Exception as e:
            print(e)
