#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for RobotAtHome API
"""

from setuptools import setup, find_packages

setup(
    name='robotathome',
    version='0.1',
    author='Gregorio Ambrosio',
    author_email='gambrosio@uma.es',
    packages=find_packages(exclude=['tests*']),
    license='LICENSE.md',
    description='This package provides Python API that assists in loading, \
    parsing, and visualizing the annotations in Robot@Home Dataset',
    long_description=open('README.md').read(),
    install_requires=['os', 'hashlib', 'humanize', 'wget',
                      'ssl', 'cv2', 'numpy', 'sys'],
    url='https://github.com/goyoambrosio/RobotAtHome_API'
)
