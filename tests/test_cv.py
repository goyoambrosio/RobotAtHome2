#!/usr/bin/env python
# -*- coding: utf-8; buffer-read-only: t -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/22"
__license__ = "MIT"

import unittest
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# from robotathome import RobotAtHome, logger, set_log_level, say_hello, hello_cv
import robotathome as rh
from robotathome import logger, set_log_level

# import os
# import sys
# import numpy as np
# from matplotlib import pyplot as plt
# import matplotlib.patches as mpatches
# import matplotlib.pyplot as plt
# import cv2
# import imagehash
# from PIL import Image
# import gluoncv as gcv

class Test(unittest.TestCase):
    """Test class of toolbox module """

    # @unittest.skip("testing skipping")
    def setUp(self):
        """ The setUp() method allow you to define instructions that will be
                executed before and after each test method

        Examples:
            python -m unittest <testModule>.<className>.<function_name>

            $ cd ~/cloud/GIT/RobotAtHome_API/tests
            $ python -m unittest test_reader.Test.test_get_home_names


        """

        # we are testing: set the lowest log level
        rh.set_log_level('TRACE')

        logger.trace("*** Test.setUp")

        # Local references
        '''
        /home/user
        └─── WORKSPACE
             ├─── R@H2-2.0.1
             │    └── files
             │        ├── rgbd
             │        └── scene
             └─────── rh.db
        '''

        self.rh_path = os.path.expanduser('~/WORKSPACE/R@H2-2.0.1')
        self.wspc_path = os.path.expanduser('~/WORKSPACE')
        self.rgbd_path = os.path.join(self.rh_path, 'files/rgbd')
        self.scene_path = os.path.join(self.rh_path, 'files/scene')
        self.db_filename = 'rh.db'

        try:
            self.rh = rh.RobotAtHome(rh_path = self.rh_path,
                                     rgbd_path = self.rgbd_path,
                                     scene_path = self.scene_path,
                                     wspc_path = self.wspc_path,
                                     db_filename = self.db_filename
                                     )
        except:
            logger.error("setUp: something was wrong")
            # exit without handling
            os._exit(1)

    def tearDown(self):
        """The tearDown() method allow you to define instructions that will be
               executed after each test method"""
        logger.trace("*** Test.tearDown")
        del self.rh

    def test_say_hello(self):
        """Testing of say_hello
        """
        logger.trace("*** Testing of say_hello()")
        logger.info("Running say_hello in _greetings.py")

        logger.info(rh.say_hello())

    def test_hello_cv(self):
        """Testing of hello_cv
        """
        logger.trace("*** Testing of hello_cv()")
        logger.info("Running hello_cv in opencv.py")

        logger.info(rh.hello_cv())


    def test_get_labeled_img(self):
        """Testing of get_labeled_img
        """
        logger.trace("*** Testing of get_labeled_img()")
        logger.info("Getting labeled image")

        id = 100000 # 100000 <= id < 200000
        [rgb_f, _] = self.rh.get_RGBD_files(id)
        labels = self.rh.get_RGBD_labels(id)
        [labeled_img, _] = rh.get_labeled_img(labels, rgb_f)
        plt.imshow(labeled_img)
        plt.show()

    def test_plot_labeled_img(self):
        """Testing of plot_labels
        """
        logger.trace("*** Testing of plot_labeled_img()")
        logger.info("Plotting RGB image patched with labels")

        set_log_level('INFO')
        id = 100000 # 100000 <= id < 200000
        [rgb_f, _] = self.rh.get_RGBD_files(id)
        labels = self.rh.get_RGBD_labels(id)
        logger.info("\nlabel names: \n{}", labels['name'])
        logger.info("\nlabel masks type: \n{}", type(labels['mask'].iat[0]))
        rh.plot_labeled_img(labels, rgb_f)


    def test_get_scan_xy(self):
        id = 200000 # 0 <= id <= inf
        laser_scan = self.rh.get_laser_scan(id)
        xy = rh.get_scan_xy(laser_scan)
        print(xy)

    def test_plot_scan(self):
        id = 200000 # 0 <= id <= inf
        laser_scan = self.rh.get_laser_scan(id)
        rh.plot_scan(laser_scan)




if __name__ == '__main__':
    unittest.main()
