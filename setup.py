#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for RobotAtHome API
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotathome",
    version="0.1.3",
    author="G. Ambrosio-Cestero",
    author_email="gambrosio@uma.es",
    description="'This package provides Python API that assists in loading, parsing, and visualizing the annotations in Robot@Home Dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goyoambrosio/RobotAtHome_API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
