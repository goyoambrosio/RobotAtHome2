#!/usr/bin/env python
# -*- coding: utf-8; buffer-read-only: t -*-

"""
Logger related functions for robotathome package
"""

import sys
from loguru import logger
from .helpers import reverse_dict

__all__=['logger', 'set_log_level',
         'log_levels', 'log_level_name', 'log_level_no',
         'get_current_log_level', 'is_being_logged'
         ]



def set_log_level(level='WARNING', sink=sys.stderr):
    logger.remove()
    logger.add(sink=sink, level=level)
    # logger.configure(handlers=[{"sink": sink, "level": level}])

def log_levels():
    log_levels_key_no = {}
    level_values = logger._core.levels.values()
    for level_value in level_values:
        log_levels_key_no[level_value.no] = level_value.name
    log_levels_key_name = reverse_dict(log_levels_key_no)
    return log_levels_key_no, log_levels_key_name

def log_level_name(level_no):
    log_levels_key_no, _ = log_levels()
    return log_levels_key_no[level_no]

def log_level_no(level_name):
    _, log_levels_key_name = log_levels()
    return log_levels_key_name[level_name]

def get_current_log_level():
    level_no = logger._core.min_level
    level_name = log_level_name(level_no)

    return level_no, level_name

def is_being_logged(level_name='DEBUG'):
    """
    This function returns True if the current logging level is under
    'level' value
    """

    current_log_level_no, _ = get_current_log_level()
    return current_log_level_no <= log_level_no(level_name)
