from .base import Base


class Shutdown(Base):

    def run(self):
        self.get(self._base_url.format('shutdown'))
