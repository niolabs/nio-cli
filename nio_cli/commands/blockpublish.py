from pprint import pprint
from os import getenv
import json
import requests

from .base import Base
from ..utils.spec import build_spec_for_block


class BlockPublish(Base):

    def run(self):
        spec = self._fetch_spec()
        if self.options.get('--dry-run'):
            pprint(spec)
            return
        self._publish_spec(spec)

    def _fetch_spec(self):
        """ Fetches the spec.json and fills in details

        Returns:
            spec (dict): The dictionary of spec info

        Raises:
            FileNotFoundError: No spec.json
        """
        output_spec = {}
        with open('spec.json', 'r') as f:
            spec = json.load(f)
        print(spec)
        for block_name, block_spec in spec.items():
            from_python = block_spec.pop('from_python', None)
            from_readme = block_spec.pop('from_readme', None)
            if from_python:
                # We will load the block spec data from the block file itself
                # Anything provided in spec.json should take precedence though
                spec_data_from_block = build_spec_for_block(from_python)
                spec_data_from_block.update(block_spec)
                block_spec = spec_data_from_block
            if from_readme:
                # Load the long description from the readme file specified
                with open(from_readme, 'r') as f:
                    block_spec['long_description'] = f.read()
            output_spec[block_name] = block_spec
        return output_spec

    def _publish_spec(self, spec):
        # Loop through the specs, we can only publish one at a time
        access_token = self.options.get('--api-token') or \
            getenv('API_ACCESS_TOKEN')
        if not access_token:
            print("ERROR: No access token specified, use the --api-token "
                  "argument or the API_ACCESS_TOKEN env var")
            return
        for block_name, block_spec in spec.items():
            print("Publishing version {} of {}".format(
                block_spec.get('version'), block_name))
            resp = requests.post(
                (self.options.get('--api-url') or
                    'https://api.n.io/v1/block/specification'),
                headers={
                    'Authorization': 'bearer {}'.format(access_token),
                },
                json={block_name: block_spec}
            )
            try:
                resp.raise_for_status()
                print(resp.json().get('message', 'No message received'))
            except Exception:
                print("ERROR: {}".format(
                    resp.json().get('message', 'Unknown error')))
