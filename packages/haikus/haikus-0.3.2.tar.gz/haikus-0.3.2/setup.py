from setuptools import setup
from pykakasi import kakasi
from setuptools import setup, find_packages
import json
# 関数のラップ


# 関数のラップ

NAME = 'haikus'
VERSION = '0.3.2'
DESCRIPTION = 'A Python package for analyzing haikus.'
LONG_DESCRIPTION = open('README.md').read()
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
URL = 'https://github.com/ituyama/haikus'
AUTHOR = 'YAMANO Itsuki'
LICENSE = 'CC BY-SA 4.0'
CLASSIFIERS = [
    'Programming Language :: Python :: 3.6'
]
INSTALL_REQUIRES = ['pykakasi']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    url=URL,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    license=LICENSE,
    install_requires=INSTALL_REQUIRES
)
