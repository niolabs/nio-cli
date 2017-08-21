import json
import os
import sys
import subprocess

from .base import Base


class BlockCheck(Base):

    # This command should be run from inside the block dir

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._directory_name = os.getcwd().split('/')[-1]
        self.run_build_spec = False

    @staticmethod
    def _read_block_files():
        block_versions = {}
        class_name = None
        block_files = [f for f in os.listdir('.') if f.endswith('.py')
                       and '__init__' not in f]
        for block in block_files:
            with open(block) as f:
                lines = [l.rstrip() for l in f.readlines()]
                for line in lines:
                    if 'class ' in line:
                        split1 = line.split(' ')[1]
                        class_name = split1.split('(')[0]
                        block_versions[class_name] = ''
                    if '= VersionProperty' in line:
                        replace1 = line.replace('"', '^')
                        replace2 = replace1.replace("'", '^')
                        version_string = replace2.split("^")[1]
                        version_list = version_string.split('.')
                        major_minor = '.'.join(
                            [version_list[0], version_list[1]])
                        block_versions[class_name] = major_minor
        return block_versions, block_files

    def run(self):
        block_versions, block_files = self._read_block_files()
        specs = self._read_spec_file()
        readme_lines = self._read_readme()
        releases = self._read_release_file()

        self.check_pep8()
        self.check_spec(specs, block_files)
        self.check_readme(readme_lines, specs)
        self.check_release(specs, releases)
        self.check_version(specs, releases, block_versions)
        self.check_naming(specs, block_versions, block_files)
        if self.run_build_spec:
            print(
                '\n**Run `nio buildspec {}` from the project directory '
                'and re-run this check**\n'.format(self._directory_name)
            )

    def _read_spec_file(self):
        specs = {}
        if os.path.exists('spec.json'):
            with open('spec.json') as f:
                try:
                    specs = json.load(f)
                except json.JSONDecodeError:
                    print('spec.json file is either incomplete or '
                          'has an invalid JSON object')
                    self.run_build_spec = True
        else:
            self.run_build_spec = True
        return specs

    @staticmethod
    def _read_readme():
        lines = []
        if os.path.exists('README.md'):
            with open('README.md') as f:
                lines = [l.rstrip() for l in f.readlines()]
        else:
            print(
                '\n**Run `nio buildreadme` as long as the spec.json file is '
                'complete.**'
            )
        return lines

    def _read_release_file(self):
        release_dict = {}
        if os.path.exists('release.json'):
            with open('release.json') as f:
                release_dict = json.load(f)
        else:
            print(
                '\n**Run `nio buildrelease {}` from the project directory as '
                'long as the spec.json file is complete.**'.format(
                    self._directory_name)
            )
        return release_dict

    def check_pep8(self):
        self.print_check('PEP8')
        shell_pep8 = 'pep8 .'
        subprocess.call(shell_pep8, shell=True)
        print('')

    def check_spec(self, specs, block_files):
        self.print_check('spec.json')
        if len(specs.keys()) > len(block_files):
            print('There are extra blocks in the spec file')
            self.run_build_spec = True

        if len(specs.keys()) < len(block_files):
            print('Not all blocks are in the spec file')
            self.run_build_spec = True

        for block in specs.keys():
            keys = ['version', 'description', 'properties']
            for key in keys:
                if key not in [k for k in specs[block]]:
                    print('{} block is missing {}'.format(block[4:], key))
                    self.run_build_spec = True
                if specs[block][key] == '':
                    print(
                        'Fill in the {} of the {} block'.format(key, block[4:])
                    )

            for prop, val in \
                    specs[block]['properties'].items():
                if val['description'] == '':
                    print(
                        'Fill in the description for the '
                        '"{}" property in the {} block'.format(prop, block[4:])
                    )
        print('')

    def check_readme(self, lines, specs):
        self.print_check('README.md')
        block_indices = []
        for block in specs.keys():
            if block[4:] not in lines:
                print('Add the {} block to the README')
            block_indices.append(lines.index(block[4:]))
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
        print('')

    def check_release(self, specs, releases):
        self.print_check('release.json')

        for block in specs.keys():
            if block not in releases:
                print('Add {} block to release.json'.format(block[4:]))
            for key in ['url', 'version', 'language']:
                if key not in releases[block] \
                        or releases[block][key] == '':
                    print('Add a {} to the {} block'.format(key, block[4:]))
        print('')

    def check_version(self, specs, releases, block_versions):
        self.print_check('version')
        for block in specs.keys():
            split_spec_version = specs[block]['version'].split('.')
            spec_version = '.'.join(
                [split_spec_version[0], split_spec_version[1]])
            if block_versions[block[4:]] != spec_version:
                print(
                    'The {} version in the spec file '
                    'does not match the version in its '
                    'block file'.format(block[4:])
                )
            split_release_version = releases[block]['version'].split('.')
            release_version = '.'.join(
                [split_release_version[0], split_release_version[1]])
            if block_versions[block[4:]] != release_version:
                print(
                    'The {} version in the release file '
                    'does not match the version in its '
                    'block file'.format(block[4:])
                )
            if spec_version != release_version:
                print(
                    'Spec.json and release.json versions do not match for '
                    '{} block'.format(block[4:])
                )
        print('')

    def check_naming(self, specs, block_versions, block_files):
        self.print_check('class and file name')
        for block in specs:
            if '_' in block:
                print(
                    '{} class name should be camelCase format'.format(
                        block[4:])
                )
            if block[4:] not in block_versions.keys():
                print(
                    '{} block needs to have a defined class'.format(block[4:])
                )

        for block in block_files:
            if not block.islower():
                print(
                    '{} file name should be lowercased and '
                    'snake_cased'.format(block[4:])
                )
        print('')

    @staticmethod
    def print_check(check):
        print('Checking {} formatting ...'.format(check))
