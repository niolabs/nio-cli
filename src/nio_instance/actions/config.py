from .base import Action
from ..util import ConfigProperty, NIOClient


EXCLUDE = ['name', 'sys_metadata', 'mappings', 'execution']


class ConfigAction(Action):

    def perform(self):
        data = {}

        # TODO: boldly unsafe - mostly the json deser
        resource = NIOClient.list(self.args.resource, self.args.name).json()
        properties = self._get_resource_props(resource)

        for prop in [b for b in properties if b not in EXCLUDE]:
            cfg_prop = ConfigProperty(prop, properties[prop], resource[prop])
            if not cfg_prop._detail.get('readonly', False):
                cfg_prop.process()
            data[prop] = cfg_prop.value

        rsp = NIOClient.config(self.args.resource, self.args.name, data)
        new_data = self.process(rsp)
        rows = self._gen_spec(new_data)
        self.generate_output(rows)

    def _get_resource_props(self, resource):
        endpoint = "{0}_types".format(self.args.resource)
        all_resources = NIOClient.list(endpoint).json()
        specific_type = resource['type']
        resource_template = all_resources[specific_type]
        return resource_template.get('properties', {})
