import json, os, sys
from nio.util.discovery import is_class_discoverable as _is_class_discoverable
from niocore.core.loader.discover import Discover
from .base import Base


def is_class_discoverable(_class, default_discoverability=True):
    return _is_class_discoverable(_class, default_discoverability)


class BuildSpec(Base):

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._repo = self.options['<repo-name>']

    def run(self):
        spec = {}
        from nio.block.base import Block
        sys.path.insert(0, os.getcwd())
        blocks = Discover.discover_classes(
            'blocks.{}'.format(self._repo), Block, is_class_discoverable)
        for block in blocks:
            k, v = self._build_spec_for_block(block)
            spec[k] = v
        with open('blocks/{}/spec.json'.format(self._repo), 'w') as f:
            json.dump(spec, f, sort_keys=True, indent=2)

    def _build_spec_for_block(self, block):
        properties = block.get_description()["properties"]
        block_spec = {}
        block_spec["Version"] = properties["version"]["default"]
        block_spec["Properties"] = {}
        for k, property in properties.items():
            if k in ['type', 'name', 'version', 'log_level']:
                continue
            property_spec = {}
            if property["default"]:
                property_spec["default"] = property["default"]
            block_spec["Properties"][property["title"]] = property_spec
        return "{}/{}".format("nio", block.__name__), block_spec
