#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup
import re


with open('naclencryptedfields/__init__.py', 'r') as init_file:
    version = re.search(
        '^__version__ = [\'"]([^\'"]+)[\'"]',
        init_file.read(),
        re.MULTILINE,
    ).group(1)


setup(
    name='nacl-encrypted-fields',
    description=(
        'This is a collection of Django Model Field classes that are encrypted'
        ' using NaCl.'
    ),
    url='https://gitlab.poolvos.nl/arjen/nacl-encrypted-fields',
    license='TODO',
    author='Arjen T. Zijlstra',
    author_email='az@warpnet.nl',
    packages=['naclencryptedfields'],
    version=version,
    install_requires=[
        'Django>=2.0',
        'PyNaCl>=1.3.0',
    ],
)
