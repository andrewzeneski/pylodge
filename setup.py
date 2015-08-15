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

    description='Test Automation framework for TestLodge',
    long_description=long_description,

    url='https://github.com/gettalent/pylodge',

    # Author details
    author='Ashwin Kondapalli',
    author_email='ashwin@gettalent.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',

    ],

    keywords='TestLodge, test automation',

    packages=find_packages(),

    install_requires=['pyOpenSSL', 'ndg-httpsclient', 'pyasn1', 'requests'],

)
make_config.create_config_file()