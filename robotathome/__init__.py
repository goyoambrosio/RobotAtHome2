#!/usr/bin/env python
# -*- coding: utf-8; buffer-read-only: t -*-

__version__ = "1.0.0"

from ._version import *
from .log import *
from .helpers import *

# from . import cv # rh.cv.say_hello
# from .cv import say_hello, hello_cv # rh.say_hello
from .cv import *
from .core import RobotAtHome

__all__=[]
__all__.extend(_version.__all__)
__all__.extend(log.__all__)
__all__.extend(helpers.__all__)
__all__.extend(core.__all__)

set_log_level('SUCCESS')
# set_log_level('DEBUG')
