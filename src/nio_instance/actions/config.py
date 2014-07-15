import re
import requests
from .base import Action
from util import LIST_FORMAT


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
        excl = ['name', 'sys_metadata']
        data = {}

        # TODO: boldly unsafe
        resource = requests.get(self.urls[0], auth=self.auth).json()
        resource_type = resource['type']
        type_url = self._create_types_url()
        all_resources = requests.get(type_url, auth=self.auth).json()
        resource_props = all_resources[resource_type].get('properties', {})
        for prop in [b for b in resource_props if b not in excl]:
            detail = resource_props[prop]
            if not detail.get('readonly', False):
                val = input("%s (%s): " % (prop, detail['type']))
                if val == '':
                    val = resource[prop]
                elif detail['type'] == 'int':
                    val = int(val)
                elif detail['type'] == 'bool':
                    val = True if re.match(r'[tT]', val) else False
                data[prop] = val

        super().perform(data)
