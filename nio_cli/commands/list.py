import json
import requests
from .base import Base


class List(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._resource = 'services' if self.options['services'] else 'blocks'
        self._resource_name = \
            self.options['<service-name>'] if self.options['services'] else \
            self.options['<block-name>'] if self.options['blocks'] else \
            ""

    def run(self):
        response = requests.get(self._base_url.format(self._resource),
                                auth=self._auth)
        try:
            [print(resource) for resource in response.json()]
        except:
            pass
