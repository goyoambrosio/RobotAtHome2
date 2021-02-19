#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get version for RobotAtHome package
"""

import os


def _read(rel_path):
    """ Docstring """
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def _get_version(rel_path):
    """ Docstring """
    for line in _read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

def get_version_str():
    """ Docstring """

    _s = "Robot@Home Dataset (" + _get_version("__init__.py") + ")" + "\n"
    _s += "============================"

    return _s
