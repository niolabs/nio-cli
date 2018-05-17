import json
import os
import sys
from collections import OrderedDict

from nio.block.base import Base as BaseBlock
from nio.util.discovery import is_class_discoverable as _is_class_discoverable
try:
    from niocore.core.loader.discover import Discover
except:
    # prevent `main` from failing on `from nio_cli import commands` if
    # `niocore` not available
    pass

from .base import Base


def is_class_discoverable(_class, default_discoverability=True):
    return _is_class_discoverable(_class, default_discoverability)


class BuildSpec(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._repo = self.options['<repo-name>']

    def run(self):
        spec = {}
        sys.path.insert(0, os.getcwd())
        blocks = Discover.discover_classes(
            'blocks.{}'.format(self._repo), BaseBlock, is_class_discoverable)
        for block in blocks:
            k, v = self._build_spec_for_block(block)
            spec[k] = v
        file_path = 'blocks/{}/spec.json'.format(self._repo)
        previous_spec = self._read_spec(file_path)
        merged_spec = self._merge_previous_into_new_spec(previous_spec, spec)
        sorted_spec = self._order_dict(merged_spec)
        with open(file_path, 'w') as f:
            json.dump(sorted_spec, f, indent=2)

    def _read_spec(self, file_path):
        if os.path.exists(file_path):
            with open(file_path) as f:
                return json.load(f)
        else:
            return {}

    def _merge_previous_into_new_spec(self, previous_spec, spec):
        for block in spec:
            manual_fields = [("description", ""), ("categories", [])]
            for field in manual_fields:
                spec[block][field[0]] = \
                    previous_spec.get(block, {}).get(field[0], field[1])
            for field in ["properties", "commands", "inputs", "outputs"]:
                for name in spec[block][field]:
                    spec[block][field][name]["description"] = \
                        previous_spec.get(block, {}).get(field, {}).\
                        get(name, {}).get("description", "")
                    for attr, value in previous_spec.get(block, {}).\
                            get(field, {}).get(name, {}).items():
                        if attr not in spec[block][field][name]:
                            spec[block][field][name][attr] = value
        return spec

    def _order_dict(self, spec):
        keyorder = [
            'version',
            'description',
            'categories',
            'properties',
            'inputs',
            'outputs',
            'commands'
        ]
        for block in spec:
            spec[block] = OrderedDict(
                sorted(
                    spec[block].items(),
                    key=lambda i: keyorder.index(i[0])
                ))
            self._alphabetical_order_dict(spec[block])
        return OrderedDict(sorted(spec.items(), key=lambda i: i[0]))

    @staticmethod
    def _alphabetical_order_dict(dict):
        for key in ['properties', 'inputs', 'outputs', 'commands']:
            dict[key] = OrderedDict(
                sorted(dict[key].items(), key=lambda  i: i[0]))
        for prop_key in dict["properties"]:
            keyorder = ["title", "type", "description", "default"]
            dict["properties"][prop_key] = OrderedDict(
                sorted(
                    dict["properties"][prop_key].items(),
                    key=lambda i: keyorder.index(i[0])
                ))
        return dict

    def _build_spec_for_block(self, block):
        block_spec = {}
        properties = block.get_description()["properties"]
        block_spec["version"] = properties["version"]["default"]
        block_spec["properties"] = self._build_properties_spec(block)
        block_spec["commands"] = self._build_commands_spec(block)
        block_spec["inputs"] = self._build_inputs_spec(block)
        block_spec["outputs"] = self._build_outputs_spec(block)
        return "{}/{}".format("nio", block.__name__), block_spec

    def _build_properties_spec(self, block):
        properties_spec = {}
        properties = block.get_description()["properties"]
        for k, property in properties.items():
            if k in ["id", "type", "name", "version", "log_level"]:
                continue
            property_spec = {}
            property_spec["title"] = property["title"]
            property_spec["type"] = property["type"]
            if "default" in property:
                property_spec["default"] = property["default"]
            properties_spec[k] = property_spec
        return properties_spec

    def _build_commands_spec(self, block):
        commands_spec = {}
        commands = block.get_description()["commands"]
        for k, command in commands.items():
            if k in ['properties']:
                continue
            command_spec = {}
            command_spec["params"] = command["params"]
            commands_spec[command["title"]] = command_spec
        return commands_spec

    def _build_inputs_spec(self, block):
        inputs_spec = {}
        inputs = block.inputs()
        for input_object in inputs:
            input_label = input_object.get_description()["label"]
            inputs_spec[input_label] = {"description": ""}
        return inputs_spec

    def _build_outputs_spec(self, block):
        outputs_spec = {}
        outputs = block.outputs()
        for output_object in outputs:
            output_label = output_object.get_description()["label"]
            outputs_spec[output_label] = {"description": ""}
        return outputs_spec
