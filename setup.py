__author__ = 'ashwin'
"""A Test Lodge based pylodge module.

"""

from setuptools import setup

setup(
    name='pylodge',
    version='0.2.8',

    description='Test Automation framework for TestLodge',

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
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',

    ],

    keywords='TestLodge, test automation, pylodge',

    packages=['pylodge'],

    install_requires=['requests'],

)
