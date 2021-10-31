"""
Logger related functions for robotathome package
"""

import sys
from loguru import logger
from .helpers import reverse_dict

__all__=['enable_logger','logger',
         'get_log_levels', 'get_log_level_name', 'get_log_level_no',
         'current_log_level', 'is_being_logged'
         ]


logger.disable("robotathome")


def enable_logger(sink=sys.stderr, level="WARNING"):
    """
    Enable the logging of messages.

    Configure the ``logger`` variable imported from ``loguru``.

    Args:
        sink (file): An opened file pointer, or stream handler. Default to
                     standard error.
        level (str): The log level to use. Possible values are TRACE, DEBUG,
                     INFO, WARNING, ERROR, CRITICAL.
                     Default to WARNING.

    (*) Extracted from aria2p project
    """
    logger.remove()
    logger.configure(handlers=[{"sink": sink, "level": level}])
    logger.enable("robotathome")

def get_log_levels():
    log_levels_key_no = {}
    level_values = logger._core.levels.values()
    for level_value in level_values:
        log_levels_key_no[level_value.no] = level_value.name
    log_levels_key_name = reverse_dict(log_levels_key_no)
    return log_levels_key_no, log_levels_key_name

def get_log_level_name(level_no):
    log_levels_key_no, _ = get_log_levels()
    return log_levels_key_no[level_no]

def get_log_level_no(level_name):
    _, log_levels_key_name = get_log_levels()
    return log_levels_key_name[level_name]

def current_log_level():
    level_no = logger._core.min_level
    level_name = get_log_level_name(level_no)

    return level_no, level_name

def is_being_logged(level_name='DEBUG'):
    """
    This function returns True if the current logging level is under
    'level' value
    """

    current_log_level_no, _ = current_log_level()
    return current_log_level_no <= get_log_level_no(level_name)
