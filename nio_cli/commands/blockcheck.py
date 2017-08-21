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
        self.block_files_including_base = [
            f for f in self.all_contents if '.py' in f
        ]
        self.block_files = [
            f for f in self.all_contents if 'block.py' in f and 'base' not in f
        ]
        self.blocks_in_spec = []
        self.spec_versions_dict = {}
        self.release_versions_dict = {}
        self.file_versions_and_names_dict = self.get_versions_and_class_names()

    def get_versions_and_class_names(self):

        name_version_dict = {
            'classes': [],
            'versions': [],
        }
        for block in self.block_files_including_base:
            with open(block) as f:
                lines = [l.rstrip() for l in f.readlines()]
                for line in lines:
                    if 'class ' in line:
                        split1 = line.split(' ')[1]
                        class_name = split1.split('(')[0]
                        name_version_dict['classes'].append(class_name)
                    if '= VersionProperty' in line:
                        replace1 = line.replace('"', '^')
                        replace2 = replace1.replace("'", '^')
                        version_string = replace2.split("^")[1]
                        name_version_dict['versions'].append(version_string[:3])
        return name_version_dict

    def run(self):

        self.print_check('PEP8')
        self.check_pep8()

        self.print_check('spec.json')
        self.check_spec()

        self.print_check('README.md')
        self.check_readme()

        self.print_check('release.json')
        self.check_release()

        self.print_check('version')
        self.check_version()

        self.print_check('class and file name')
        self.check_naming()

    def check_pep8(self):

        shell_pep8 = 'pep8 .'
        subprocess.call(shell_pep8, shell=True)
        print('')

    def check_spec(self):

        if os.path.exists('spec.json'):
            with open('spec.json') as f:
                try:
                    spec_dict = json.load(f)
                except json.JSONDecodeError:
                    print('spec.json file is either incomplete or '
                          'has an invalid JSON object')
                    print(
                        '\n**Run `nio buildspec {}` '
                        'from the project directory '
                        'and re-run this check**\n'.format(self._block)
                    )
                    sys.exit()
                self.blocks_in_spec = [
                    k.split('/')[1] for k, v in spec_dict.items()
                ]

            if len(self.blocks_in_spec) > len(self.block_files):
                print('There are extra blocks in the spec file')
                print(
                    '\n**Run `nio buildspec {}` from the project directory '
                    'and re-run this check**\n'.format(self._block)
                )
                sys.exit()
            if len(self.blocks_in_spec) < len(self.block_files):
                print('Not all blocks are in the spec file')
                print(
                    '\n**Run `nio buildspec {}` from the project directory '
                    'and re-run this check**\n'.format(self._block)
                )
                sys.exit()

            for block in self.blocks_in_spec:
                self.spec_versions_dict[block] = \
                    spec_dict['nio/' + block]['version']
                keys = ['version', 'description', 'properties', 'inputs',
                        'outputs', 'commands']
                for key in keys:
                    if key not in [k for k in spec_dict['nio/' + block]]:
                        print('{} block is missing {}'.format(block, key))
                        print(
                            '\n**Run `nio buildspec {}` '
                            'from the project directory '
                            'and re-run this check**\n'.format(self._block)
                        )
                    if key in ['commands', 'inputs', 'outputs']:
                        continue
                    if not spec_dict['nio/' + block][key] \
                            or spec_dict['nio/' + block][key] == '':
                        print('Fill in the {} of the {} block'.format(
                            key, block))

                for prop, val in \
                        spec_dict['nio/' + block]['properties'].items():
                    if val['description'] == '':
                        print(
                            'Fill in the description for the '
                            '"{}" property in the {} block'.format(prop, block)
                        )
        else:
            print(
                '\n**Run `nio buildspec {}` from the project directory '
                'and re-run this check**\n'.format(self._block)
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
                    print('Add the {} block to the README')
                block_indices.append(lines.index(block))
            block_indices.sort()

            for i in range(len(block_indices)):
                for key in ['Properties', 'Inputs', 'Outputs',
                            'Commands', 'Dependencies']:
                    try:
                        if key not in \
                                lines[block_indices[i]:block_indices[i+1]]:
                            print('Add "{}" to the {} block'.format(
                                key, lines[block_indices[i]]))
                    except IndexError:
                        if key not in lines[block_indices[i]:]:
                            print('Add "{}" to the {} block'.format(
                                key, lines[block_indices[i]]))
        else:
            print(
                'Run `nio buildreadme` '
                'as long as the spec.json file is complete'
            )
        print('')

    def check_release(self):

        if os.path.exists('release.json'):
            with open('release.json') as f:
                release_dict = json.load(f)

        for block in self.blocks_in_spec:
            if 'nio/' + block not in release_dict:
                print('Add {} block to release.json'.format(block))
            for key in ['url', 'version', 'language']:
                if key not in release_dict['nio/' + block] \
                        or release_dict['nio/' + block][key] == '':
                    print('Add a {} to the {} block'.format(key, block))
            self.release_versions_dict[block] = \
                release_dict['nio/' + block]['version']
        print('')

    def check_version(self):

        for block in self.blocks_in_spec:
            if self.release_versions_dict[block][:3] != \
                    self.spec_versions_dict[block][:3]:
                print(
                    'Spec.json and release.json versions do not match for '
                    '{} block'.format(block)
                )
            if self.release_versions_dict[block][:3] \
                    not in self.file_versions_and_names_dict['versions']:
                print(
                    'The {} version in the release file '
                    'does not match the version in its '
                    'block file'.format(block)
                )
                if self.spec_versions_dict[block][:3] \
                    not in self.file_versions_and_names_dict['versions']:
                    print(
                        'The {} version in the spec file '
                        'does not match the version in its '
                        'block file'.format(block)
                    )
        print('')

    def check_naming(self):

        for block in self.blocks_in_spec:
            if '_' in block:
                print(
                    '{} class name should be camelCased format'.format(block)
                )
            if block not in self.file_versions_and_names_dict['classes']:
                print(
                    '{} block needs to have a defined class'.format(block)
                )

        for block in self.block_files:
            if not block.islower():
                print(
                    '{} file name should be lowercased and '
                    'snake_cased'.format(block)
                )
        print('')

    @staticmethod
    def print_check(check):

        print('Checking {} formatting ...'.format(check))
