import json
import os
import sys
import subprocess
import re

from .base import Base


class BlockCheck(Base):

    # This command should be run from inside the block dir

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self._directory_name = os.getcwd().split('/')[-1]
        self._run_build_spec = False
        self.block_versions, self.block_files = self._read_block_files()
        self.specs = self._read_spec_file()
        self.readme_lines = self._read_readme()
        self.releases = self._read_release_file()

    def run(self):
        self.check_pep8()
        self.check_spec()
        self.check_readme()
        self.check_release()
        self.check_version()
        self.check_naming()
        if self._run_build_spec:
            print(
                '\n**Run `nio buildspec {}` from the project directory '
                'and re-run this check**\n'.format(self._directory_name)
            )

    def _read_block_files(self):
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
                        major_minor = re.search(
                            r"VersionProperty\(['\"](\d+\.\d+)\.[^)]*\)",
                            line
                        ).group(1)
                        block_versions[class_name] = major_minor
        return block_versions, block_files

    def _read_spec_file(self):
        specs = {}
        if os.path.exists('spec.json'):
            with open('spec.json') as f:
                try:
                    specs = json.load(f)
                except json.JSONDecodeError:
                    print('spec.json file is either incomplete or '
                          'has an invalid JSON object')
                    self._run_build_spec = True
        else:
            self._run_build_spec = True
        return specs

    def _read_readme(self):
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
        self._print_check('PEP8')
        shell_pep8 = 'pep8 .'
        subprocess.call(shell_pep8, shell=True)
        print('')

    def check_spec(self):
        self._print_check('spec.json')
        if len(self.specs.keys()) > len(self.block_files):
            print('There are extra blocks in the spec file')
            self._run_build_spec = True

        if len(self.specs.keys()) < len(self.block_files):
            print('Not all blocks are in the spec file')
            self._run_build_spec = True

        for block in self.specs.keys():
            keys = ['version', 'description', 'properties']
            for key in keys:
                if key not in [k for k in self.specs[block]]:
                    print('{} block is missing {}'.format(block[4:], key))
                    self._run_build_spec = True
                if self.specs[block][key] == '':
                    print(
                        'Fill in the {} of the {} block'.format(key, block[4:])
                    )

            for prop, val in \
                    self.specs[block]['properties'].items():
                if val['description'] == '':
                    print(
                        'Fill in the description for the '
                        '"{}" property in the {} block'.format(prop, block[4:])
                    )
        print('')

    def check_readme(self):
        self._print_check('README.md')
        block_indices = []
        for block in self.specs.keys():
            if block[4:] not in self.readme_lines:
                print('Add the {} block to the README')
            block_indices.append(self.readme_lines.index(block[4:]))
        block_indices.sort()
        for i in range(len(block_indices)):
            for key in ['Properties', 'Inputs', 'Outputs',
                        'Commands', 'Dependencies']:
                try:
                    if key not in self.readme_lines[
                                  block_indices[i]:block_indices[i+1]]:
                        print('Add "{}" to the {} block'.format(
                            key, self.readme_lines[block_indices[i]]))
                except IndexError:
                    if key not in self.readme_lines[block_indices[i]:]:
                        print('Add "{}" to the {} block'.format(
                            key, self.readme_lines[block_indices[i]]))
        print('')

    def check_release(self):
        self._print_check('release.json')

        for block in self.specs.keys():
            if block not in self.releases:
                print('Add {} block to release.json'.format(block[4:]))
            for key in ['url', 'version', 'language']:
                if key not in self.releases[block] \
                        or self.releases[block][key] == '':
                    print('Add a {} to the {} block'.format(key, block[4:]))
        print('')

    def check_version(self):
        self._print_check('version')
        for block in self.specs.keys():
            split_spec_version = self.specs[block]['version'].split('.')
            spec_version = '.'.join(
                [split_spec_version[0], split_spec_version[1]])
            if self.block_versions[block[4:]] != spec_version:
                print(
                    'The {} version in the spec file does not match the '
                    'version in its block file'.format(block[4:])
                )
            split_release_version = self.releases[block]['version'].split('.')
            release_version = '.'.join(
                [split_release_version[0], split_release_version[1]])
            if self.block_versions[block[4:]] != release_version:
                print(
                    'The {} version in the release file does not match the '
                    'version in its block file'.format(block[4:])
                )
            if spec_version != release_version:
                print(
                    'Spec.json and release.json versions do not match for '
                    '{} block'.format(block[4:])
                )
        print('')

    def check_naming(self):
        self._print_check('class and file name')
        for block in self.specs:
            if '_' in block:
                print(
                    '{} class name should be camelCase format'.format(
                        block[4:])
                )
            if block[4:] not in self.block_versions.keys():
                print(
                    '{} block needs to have a defined class'.format(block[4:])
                )

        for block in self.block_files:
            if not block.islower():
                print(
                    '{} file name should be lowercased and '
                    'snake_cased'.format(block[4:])
                )
        print('')

    def _print_check(self, check):
        print('Checking {} formatting ...'.format(check))
