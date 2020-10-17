#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/10/12"
__license__ = "MIT"

# import robotathome.dataset

from robotathome.dataset import Dataset

rhds = Dataset("MyRobot@Home")

# rhds = Dataset("MyRobot@Home", autoload=False)
# rhds.unit["chelmnts"].load_data()
# rhds.unit["2dgeomap"].load_data()

# print(rhds.unit["chelmnts"])
# print(rhds.unit["2dgeomap"])

print(rhds)
