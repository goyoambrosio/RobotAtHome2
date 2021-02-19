#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for RobotAtHome API
"""

import os
import sys

from setuptools import find_packages, setup

def read(rel_path):
    """ Docstring """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    """ Docstring """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="robotathome",
    version=get_version("robotathome/__init__.py"),
    description="This package provides a Python API that assists in loading and parsing the annotations in Robot@Home Dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/goyoambrosio/RobotAtHome_API",
    keywords=('semantic mapping '
              'object categorization '
              'object recognition '
              'room categorization '
              'room recognition '
              'contextual information '
              'mobile robots '
              'domestic robots '
              'home environment '
              'robotic dataset benchmark '
              ),

    author="G. Ambrosio-Cestero",
    author_email="gambrosio@uma.es",

    packages=find_packages(),

    install_requires=[
        "humanize >= 3.0.0",
        "numpy",
        "click >= 7.1.2",
        "urllib3 >= 1.25.10",
        "loguru"
    ],

    python_requires='>=3.7',
)
