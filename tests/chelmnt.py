#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/10/12"
__license__ = "MIT"

#import robotathome.dataset
from robotathome.dataset import Dataset
import os

rhds = Dataset("MyRobot@Home")

rhds.unit["chelmnts"].load_data()

print(rhds)

