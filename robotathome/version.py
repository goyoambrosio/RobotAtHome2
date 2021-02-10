#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Get version for RobotAtHome package
"""

import os

def read(rel_path):
    """ Docstring """
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    """ Docstring """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

def get_version_str():
    """ Docstring """

    _s = "Robot@Home Dataset (" + get_version("__init__.py") + ")" + "\n"
    _s += "============================"

    return _s
