from pprint import pprint
from os import getenv
import json
import requests

from .base import Base
from ..utils.spec import build_spec_for_block, build_release_for_block


class PublishBlock(Base):

    def run(self):
        spec = self._fetch_spec()
        release = self._fetch_release()
        if self.options.get('--dry-run'):
            print("Specification that will be published:")
            pprint(spec)
            print("Release data that will be published:")
            pprint(release)
            return
        self._publish_spec(spec)
        self._publish_release(release)

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

    def _fetch_release(self):
        output_release = {}
        with open('release.json', 'r') as f:
            release = json.load(f)
        for block_name, release_info in release.items():
            from_python = release_info.pop('from_python', None)
            if from_python:
                # We will load the block release data from the block file
                # itself but anything provided in release.json should
                # take precedence though
                release_data_from_block = build_release_for_block(from_python)
                release_data_from_block.update(release_info)
                release_info = release_data_from_block
            output_release[block_name] = release_info
        return output_release

    def _publish_spec(self, spec):
        # Loop through the specs, we can only publish one at a time
        for block_name, block_spec in spec.items():
            print("Publishing version {} of {}".format(
                block_spec.get('version'), block_name))
            resp_json = self._make_request('specification', {
                block_name: block_spec
            })
            print(resp_json.get('message', 'No message received'))

    def _publish_release(self, release):
        for block_name, release_info in release.items():
            print("Publishing release {} of {}".format(
                release_info.get('version'), block_name))
            resp_json = self._make_request('release', {
                block_name: release_info
            })
            print(resp_json.get('message', 'No message received'))

    def _get_token(self):
        access_token = self.options.get('--api-token') or \
            getenv('API_ACCESS_TOKEN')
        if not access_token:
            raise RuntimeError("No access token specified, use the --api-token"
                               " argument or the API_ACCESS_TOKEN env var")
        return access_token

    def _make_request(self, path, body):
        resp = requests.post("{}/{}".format(
            self.options.get('--api-url') or 'https://api.n.io/v1/block',
            path),
            headers={
                'Authorization': 'bearer {}'.format(self._get_token()),
            },
            json=body,
        )
        try:
            resp.raise_for_status()
            return resp.json()
        except Exception:
            raise RuntimeError("ERROR: {}".format(
                resp.json().get('message', 'Unknown error')))
