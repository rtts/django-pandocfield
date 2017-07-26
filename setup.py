#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

setup(
    name = 'django-pandocfield',
    version = '0.2.5',
    url = 'https://github.com/JaapJoris/django-pandocfield',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'django',
        'bleach',
    ],
)
