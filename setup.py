"""Sets up the package"""

#!/usr/bin/env python
 # -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='bank-sim-server',
    version='0.1.0',
    description='Bank simulation using Django',
    long_description=README,
    author='Karthik Korrapaty',
    author_email='kkorrapatyjr@gmail.com',
    url= 'https://github.com/kkorrapaty/bank-sim-server',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
