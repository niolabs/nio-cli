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
        exclude = ['name', 'sys_metadata', 'mappings', 'execution']
        data = {}

        # TODO: boldly unsafe - mostly the json deser
        resource = requests.get(self.urls[0], auth=self.auth).json()
        resource_type = resource['type']
        type_url = self._create_types_url()
        all_resources = requests.get(type_url, auth=self.auth).json()
        resource_props = all_resources[resource_type].get('properties', {})

        for prop in [b for b in resource_props if b not in exclude]:
            detail = resource_props[prop]
            _type = detail['type']
            if not detail.get('readonly', False):
                val = self._process_property(prop, detail, resource[prop])
                data[prop] = val

        super().perform(data)

    def _process_property(self, name, detail, original, prompt="\n{0} ({1}): "):
        result = ''
        _type = detail['type']

        # TODO: define semantics for adding to lists
        if _type == 'list':
            return result

        # handle an object property gracefully
        elif _type == 'object':
            result = {}
            template = detail['template']
            print(prompt.format(name, _type))
            
            # prompt for a value for each of the sub-properties
            for key in template:
                result[key] = self._process_property(
                    key, template[key], original[key], "+->{0} ({1}): "
                )

        # otherwise, just a lonely field
        else:
            result = self._process_field(name, _type, original, prompt)

        return result
        
    # if a field is left blank, leave the property's value unchanged
    def _process_field(self, name, _type, original, prompt):
        result = input(prompt.format(name, _type)) 
        if result == '':
            result = original
            print('Using current value:', result)
        elif _type == 'int':
            result = int(result)
        elif _type == 'bool':
            result = True if re.match(r'[tT]', result) else False
        return result
