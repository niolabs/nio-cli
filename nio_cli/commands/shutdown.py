import requests

from .base import Base


class Shutdown(Base):

    def run(self):
        requests.get(self._base_url.format('shutdown'), auth=self._auth)
