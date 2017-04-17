import sys
import re
from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

with open('nio_cli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='nio-cli',
    version=version,
    description='Command line tools for n.io',
    url='https://github.com/nioinnovation/nio-cli',
    author='n.io',
    author_email='info@n.io',
    keywords=['nio'],
    packages=find_packages(exclude=['docs', 'tests', 'tests.*']),
    install_requires=['prettytable', 'requests', 'docopts'],
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'nio=nio_cli.cli:main'
        ]
    },
)
