from setuptools import setup, find_packages

from nio_cli import __version__

setup(
    name='nio-cli',
    version=__version__,
    description='Command line tools for n.io',
    url='https://github.com/nioinnovation/nio-cli',
    author='n.io',
    author_email='info@n.io',
    keywords=['nio'],
    packages=find_packages(exclude=['docs', 'tests', 'tests.*']),
    install_requires=['prettytable', 'requests', 'docopts'],
    entry_points={
        'console_scripts': [
            'nio=nio_cli.cli:main'
        ]
    },
)
