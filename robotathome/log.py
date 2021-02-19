"""
Logger related functions for robotathome package

This script requires that `loguru` be installed within the Python
environment you are running this script in.

Install with:
    conda install -c conda-forge loguru
    pip install loguru

"""

import sys
# import loguru
from loguru import logger

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

