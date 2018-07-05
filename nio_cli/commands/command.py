from .base import Base


class Command(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._command_name = self.options['<command-name>']
        self._service_name = self.options['<service-name>']
        self._block_name = self.options['<block-name>']

    def run(self):
        command = self._command_name
        if self._block_name:
            command = self._block_name + "/" + command
        if self._service_name:
            command = "services/" + self._service_name + "/" + command
        self.post(self._base_url.format(command))
