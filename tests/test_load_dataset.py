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

# rhds = Dataset("MyRobot@Home")
# rhds = Dataset("MyRobot@Home", path="..")

# rhds = Dataset("MyRobot@Home", path="..", autoload=False)
rhds = Dataset("MyRobot@Home", autoload=False)
# rhds.unit["chelmnts"].load_data()
# rhds.unit["2dgeomap"].load_data()
# rhds.unit["hometopo"].load_data()
# rhds.unit["raw"].load_data()
# rhds.unit["lsrscan"].load_data()
# rhds.unit["rgbd"].load_data()
# rhds.unit["lblrgbd"].load_data()
# rhds.unit["lblscene"].load_data()
rhds.unit["rctrscene"].load_data()

# print(rhds.unit["chelmnts"])
# print(rhds.unit["2dgeomap"])
# print(rhds.unit["hometopo"])
# print(rhds.unit["raw"])
# print(rhds.unit["lsrscan"])
# print(rhds.unit["rgbd"])
# print(rhds.unit["lblrgbd"])
print(rhds.unit["rctrscene"])

# rhds.unit["chelmnts"].check_folder_size(True)
# rhds.unit["2dgeomap"].check_folder_size(True)
# rhds.unit["hometopo"].check_folder_size(True)
# rhds.unit["raw"].check_folder_size(True)
# rhds.unit["lsrscan"].check_folder_size(True)
# rhds.unit["rgbd"].check_folder_size(True)
# rhds.unit["lblrgbd"].check_folder_size(True)
# rhds.unit["lblscene"].check_folder_size(True)
# rhds.unit["rctrscene"].check_folder_size(True)

print(rhds)
