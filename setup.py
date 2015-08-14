__author__ = 'ashwin'
"""A Test Lodge based pylodge module.

"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from pylodge import make_config



here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylodge',
    version='0.1',

    description='Test Automation plugin for Test Lodge',
    long_description=long_description,

    url='https://github.com/Veechi/pylodge',

    # Author details
    author='Ashwin Kondapalli',
    author_email='ashwin@gettalent.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        'Development Status :: 3 - Alpha',
        'Intended Audience :: QA',
        'Topic :: Test Automation :: Integration Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='TestLodge, test automation',

    packages=find_packages(),

    install_requires=['requests'],



)
make_config.create_config_file()