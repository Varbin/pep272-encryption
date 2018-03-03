"""
Installation script of pep272-encryption.
Usage (pip):
    pip install .
Usage (direct):
    setup.py build  # "Build" + Checkup
    setup.py install  # Installation
"""

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    sys.stderr.write("Warning: setuptools not found! "
                     "Falling back to raw distutils.\n")
    sys.stderr.write(" -> This may not properly register packages "
                     "within python.\n\n")

with open('pep272_encryption/version.py') as version_file:
    exec(version_file.read())

description='Library for easy creation of PEP-272 cipher classes'

try:
    with open('README.rst') as description_file:
        long_description = description_file.read()
except:
    long_description = description
        

args = dict(
    name='pep272-encryption',
    version=__version__,
    author=__author__,
    author_email=__email__,
    license=__license__,
    url=__url__,

    description=description,
    long_description=long_description,

    packages=['pep272_encryption'],
    classifiers = [
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

try:
    with open('README.rst', encoding='UTF-8') as readme:
        args['description_long'] = readme.read()
except:
    args['description_long'] = args['description']

setup(**args)
