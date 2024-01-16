#!/usr/bin/env python

import sys

from setuptools import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='rps-milea-users',
    version='0.1.3',
    author='red-pepper-services',
    author_email='pypi@schiegg.at',
    url='https://github.com/milea-framework/milea-users',
    license='MIT',
    description="Django rps.Milea Framework - User Module",
    long_description=long_description,
    include_package_data=True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
