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
        exclude = ['name', 'sys_metadata']
        data = {}

        # TODO: boldly unsafe - mostly the json deser
        resource = requests.get(self.urls[0], auth=self.auth).json()
        print(resource)
        resource_type = resource['type']
        type_url = self._create_types_url()
        all_resources = requests.get(type_url, auth=self.auth).json()
        resource_props = all_resources[resource_type].get('properties', {})

        for prop in [b for b in resource_props if b not in exclude]:
            detail = resource_props[prop]
            _type = detail['type']
            if not detail.get('readonly', False):
                val = self._process_property(prop, detail)
                data[prop] = val if val != '' else resource[prop]

        super().perform(data)

    def _process_property(self, name, detail, prompt="{0} ({1}):"):
        result = None
        _type = detail['type']
        if _type == 'list':
            # TODO: define semantics for adding to lists
            return result
        elif _type == 'object':
            print(prompt.format(name, _type))
            result = {}
            template = detail['template']
            for key in template:
                result[key] = self._process_property(key, template[key],
                                                     "+->{0} ({1}):")
        else:
            result = input(prompt.format(name, _type)) 
            if _type == 'int':
                result = int(result)
            elif _type == 'bool':
                result = True if re.match(r'[tT]', result) else False

        return result
