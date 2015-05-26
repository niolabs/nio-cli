from setuptools import setup, find_packages
import re

version = ''
# Auto detect the version from the __init__.py file
with open('nio_cli/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='nio-cli',

    version=version,

    description='Command line tools for n.io',

    url='https://github.com/neutralio/nio-cli',

    author='n.io',
    author_email='info@n.io',

    packages=find_packages(exclude=["tests", "tests.*"]),

    install_requires=[
        'prettytable',
        'requests'
    ],

    entry_points={
        'console_scripts': [
            'nio=nio_cli.main:_nio_instance_main'
        ]
    },

    keywords=['nio']
)
