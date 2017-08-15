import json, os, re
import subprocess
from collections import defaultdict

from .base import Base




class BlockCheck(Base):

    # This should be run from inside the block dir

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._block = os.getcwd().split('/')[-1]
        self.all_contents = os.listdir('.')
        self.block_files = [f for f in self.all_contents if 'block.py' in f and 'base' not in f]
        self.blocks_in_spec = []

    def run(self):
        # OK to assume each block has a corresponding file and each file only has one block?
        # OK that everything uses `print` statements?
        # Checks built off spec (self.blocks_in_spec)

        self.print_check('PEP8')
        self.check_pep8()

        self.print_check('spec.json')
        self.check_spec()

        self.print_check('README.md')
        self.check_readme()

        self.print_check('release.json')
        self.check_release()

        self.print_check('version')
        # check that all versions sync'd; block, release, spec
        # this should

        self.print_check('class and file name')
        # check classes for camel case, blocks for snake case

    def check_pep8(self):

        shell_pep8 = 'pep8 .'
        subprocess.call(shell_pep8, shell=True)
        print('')
        # TODO: control output of pep8 command
            # would be nice to know if no issues was present

    def check_spec(self):

        if os.path.exists('spec.json'):
            with open('spec.json') as f:
                spec_dict = json.load(f)
                self.blocks_in_spec = [k.split('/')[1] for k,v in spec_dict.items()]

            if len(self.blocks_in_spec) > len(self.block_files):
                print('There\'s extra blocks in the spec file')
            if len(self.blocks_in_spec) < len(self.block_files):
                print('Not all blocks are in the spec file')

            for block in self.blocks_in_spec:
                keys = ['version', 'description', 'properties', 'inputs',
                        'outputs', 'commands']
                for key in keys:
                    if key not in [k for k in spec_dict['nio/' + block]]:
                        print('{} block is missing {}'.format(block, key))

                for key in ['version', 'description', 'properties']:
                    if not spec_dict['nio/' + block][key] or spec_dict['nio/' + block][key] == '':
                        print('Please fill in the {}'.format(key))

                for prop,val in spec_dict['nio/' + block]['properties'].items():
                    if val['description'] == '':
                        print('Please fill in the description for the "{}" property in the {} block'.format(prop, block))

        else:
            print('Please run `nio buildspec {}` from the project directory'.format(self._block))
        print('')

    def check_readme(self):

        if os.path.exists('README.md'):
            with open('README.md') as f:
                lines = [l.rstrip() for l in f.readlines()]
            block_indices = []
            for block in self.blocks_in_spec:
                if block not in lines:
                    print('Please add the {} block to the README')
                block_indices.append(lines.index(block))
            block_indices.sort()

            # for key in ['Properties', 'Inputs', 'Outputs', 'Commands', 'Dependencies']:
            #     if key not in lines[block_index:]:
            #         pass
            #         print('Please add "{}" to the {} block'.format(key, block))
            # prev_block_index = block_index
        else:
            print('Please run `nio buildreadme` as long as the spec.json file is complete')
        print('')

    def check_release(self):
        if os.path.exists('release.json'):
            with open('release.json') as f:
                release_dict = json.load(f)

        for block in self.blocks_in_spec:
            if 'nio/' + block not in release_dict:
                print('Please add {} block to release.json'.format(block))
            for key in ['url', 'version', 'language']:
                if key not in release_dict['nio/' + block] or release_dict['nio/' + block][key] == '':
                    print('Please add a {} to the {} block'.format(key, block))
        print('')

    def check_version(self):
        pass

    def check_naming(self):
        pass

    def print_check(self, check):
        print('Checking {} formatting ...'.format(check))
