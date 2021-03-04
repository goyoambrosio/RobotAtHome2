#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/10/12"
__license__ = "MIT"

# import robotathome.dataset

from robotathome.dataset import Dataset
import cv2


rhds = Dataset("MyRobot@Home", path=".", autoload=False)
rhds.unit["lblrgbd"].load_data()
