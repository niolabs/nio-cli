from .base import Base


class Clone(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._resource = 'services'
        self._from_name = self.options['<service-name>']
        self._to_name = self.options['<new-name>']

    def run(self):
        response = self.get(
            self._base_url.format(
                '{}/{}'.format(self._resource, self._from_name)))
        try:
            new_config = response.json()
            new_config['name'] = self._to_name
            self.post(
                self._base_url.format(self._resource),
                json=new_config)
        except Exception as e:
            print(e)
