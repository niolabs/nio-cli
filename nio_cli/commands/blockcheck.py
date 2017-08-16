import json
import os
import sys
import subprocess

from .base import Base


class BlockCheck(Base):

    # This should be run from inside the block dir

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._block = os.getcwd().split('/')[-1]
        self.all_contents = os.listdir('.')
        self.block_files = [
            f for f in self.all_contents if 'block.py' in f and 'base' not in f
        ]
        self.blocks_in_spec = []
        self.spec_versions_dict = {}
        self.release_versions_dict = {}

    def run(self):
        # Questions;
        # OK to assume each block has a corresponding file and each file only has one block?
        # OK that everything uses `print` statements?
            # How can I test this?
                # Switch to having check_x methods return a string, then print that string?
        # Ok that all checks are built off the spec (self.blocks_in_spec)?
            # Would it be better to base checks off the block file(s)?

        self.print_check('PEP8')
        self.check_pep8()

        self.print_check('spec.json')
        # use `sys.exit()` for "failures" in check_spec() because
        # the checks after check_spec all use self.blocks_in_spec
        self.check_spec()

        self.print_check('README.md')
        self.check_readme()

        self.print_check('release.json')
        self.check_release()

        # TODO: Check that block file version is the same as spec/release
        self.print_check('version')
        self.check_version()

        # What should I check for in regards to naming specifications?
        self.print_check('class and file name')
        self.check_naming()

    def check_pep8(self):

        shell_pep8 = 'pep8 .'
        subprocess.call(shell_pep8, shell=True)
        print('')
        # Any way to grab pep8 output?

    def check_spec(self):

        if os.path.exists('spec.json'):
            with open('spec.json') as f:
                spec_dict = json.load(f)
                self.blocks_in_spec = [
                    k.split('/')[1] for k, v in spec_dict.items()
                ]

            if len(self.blocks_in_spec) > len(self.block_files):
                print('There\'s extra blocks in the spec file')
                sys.exit()
            if len(self.blocks_in_spec) < len(self.block_files):
                print('Not all blocks are in the spec file')
                sys.exit()

            for block in self.blocks_in_spec:
                keys = ['version', 'description', 'properties', 'inputs',
                        'outputs', 'commands']
                for key in keys:
                    if key not in [k for k in spec_dict['nio/' + block]]:
                        print('{} block is missing {}'.format(block, key))
                        sys.exit()
                self.spec_versions_dict[block] = \
                    spec_dict['nio/' + block]['version']

            for key in ['version', 'description', 'properties']:
                if not spec_dict['nio/' + block][key] \
                        or spec_dict['nio/' + block][key] == '':
                    print('Please fill in the {} of the {} block'.format(
                        key, block))
                    sys.exit()

                for prop, val in \
                        spec_dict['nio/' + block]['properties'].items():
                    if val['description'] == '':
                        print(
                            'Please fill in the description for the '
                            '"{}" property in the {} block'.format(prop, block)
                        )
                        sys.exit()
        else:
            print(
                'Please run `nio buildspec {}` '
                'from the project directory'.format(self._block)
            )
            sys.exit()
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

            for i in range(len(block_indices)):
                # TODO: better way to handle `i+1` IndexError?
                    for key in ['Properties', 'Inputs', 'Outputs',
                                'Commands', 'Dependencies']:
                        try:
                            if key not in lines[block_indices[i]:block_indices[i+1]]:
                                print('Please add "{}" to the {} block'.format(
                                    key, lines[block_indices[i]]))
                        except IndexError:
                            if key not in lines[block_indices[i]:]:
                                print('Please add "{}" to the {} block'.format(
                                    key, lines[block_indices[i]]))
        else:
            print(
                'Please run `nio buildreadme` '
                'as long as the spec.json file is complete'
            )
        print('')

    def check_release(self):
        if os.path.exists('release.json'):
            with open('release.json') as f:
                release_dict = json.load(f)

        for block in self.blocks_in_spec:
            if 'nio/' + block not in release_dict:
                print('Please add {} block to release.json'.format(block))
            for key in ['url', 'version', 'language']:
                if key not in release_dict['nio/' + block] \
                        or release_dict['nio/' + block][key] == '':
                    print('Please add a {} to the {} block'.format(key, block))
            self.release_versions_dict[block] = release_dict['nio/' + block]['version']
        print('')

    def check_version(self):
        # TODO: also check version inside block file
        for block in self.blocks_in_spec:
            if self.release_versions_dict[block] != self.spec_versions_dict[block]:
                print('Versions do not match for {} block'.format(block))
        print('')

    def check_naming(self):
        # TODO: also check class name inside block file
        for block in self.blocks_in_spec:
            if '_' in block:
                print('{} class name should be camel-cased format'.format(block))

        for block in self.block_files:
            if '_block.py' not in block:
                print('Please add _block.py to the end of the {} block filename'.format(block))
            if not block.islower():
                print('{} file name should be lowercased and kebab formatted'.format(block))
        print('')

    def print_check(self, check):
        print('Checking {} formatting ...'.format(check))
