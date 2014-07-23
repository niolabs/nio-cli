import requests
from .base import Action
from util import LIST_FORMAT, ConfigProperty


class ConfigAction(Action):

    def __init__(self, args):
        super().__init__(args, 'PUT')

    def _create_url(self):
        return [LIST_FORMAT.format(self.args.host, self.args.port,
                                   self.args.resource, self.args.name)]

    def _create_types_url(self):
        return LIST_FORMAT.format(self.args.host, self.args.port,
                                  "%s_types" % self.args.resource, '')
        
    def perform(self, data=None):
        exclude = ['name', 'sys_metadata', 'mappings', 'execution']
        data = {}

        # TODO: boldly unsafe - mostly the json deser
        resource = requests.get(self.urls[0], auth=self.auth).json()
        properties = self._get_resource_props(resource)

        for prop in [b for b in properties if b not in exclude]:
            cfg_prop = ConfigProperty(prop, properties[prop], resource[prop])
            if not cfg_prop._detail.get('readonly', False):
                cfg_prop.process()
            data[prop] = cfg_prop.value

        super().perform(data)

    def _get_resource_props(self, resource):
        resource_type = resource['type']
        type_url = self._create_types_url()
        all_resources = requests.get(type_url, auth=self.auth).json()
        return all_resources[resource_type].get('properties', {})
