#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test functions for helpers.py

This module contains a Test class with methods to test functions of helpers.py
Test class conforms to the unittest framework.
"""

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/09/13"
__license__ = "MIT"

import unittest
import os
import sys
import robotathome as rh


class Test(unittest.TestCase):
    """ Test class of helpers module"""

    def setUp(self):
        """ The setUp() method allow you to define instructions that will be
                executed before and after each test method

        Examples:
            python -m unittest <testModule>.<className>.<function_name>

            $ cd ~/Dropbox/GIT/RobotAtHome_API/tests
            $ python -m unittest test_helpers.Test.test_download


        """

        # rh.logger.info("""
        # Remember:
        # python -m unittest <testModule>.<className>.<function_name>
        # e.g.
        # cd ~/Dropbox/GIT/RobotAtHome_API/tests
        # python -m unittest test_helpers.Test.test_download
        # """)

        rh.log.enable_logger(sink=sys.stderr, level="TRACE")
        rh.logger.trace("*** Test.setUp")

    def tearDown(self):
        """The tearDown() method allow you to define instructions that will be
               executed before each test method"""
        rh.logger.trace("*** Test.tearDown")

    def test_download(self):
        """Testing download(url, filename) function

        Example:
            $ python -m unittest test_helpers.Test.test_download
        """

        rh.logger.trace("*** Testing download")

        # Download of Robot@Home2_db.tgz
        url = 'https://zenodo.org/record/4530453/files/Robot@Home2_db.tgz?download=1'
        rh.logger.info("Downloading from {}", url)
        rh.download(url, '~/WORKSPACE')

        # Download Robot@Home2_files.tgz
        # url = 'https://zenodo.org/record/4530453/files/Robot@Home2_files.tgz?download=1'
        # rh.logger.info("Downloading from {}", url)
        # rh.download(url, '~/WORKSPACE')


    def test_get_md5(self):
        """Testing get_md5(filename)

        Example:
            $ python -m unittest test_helpers.Test.test_get_md5
        """

        rh.logger.trace("*** Testing get_md5")
        rh.logger.info("Computing MD5 hash value of Robot@Home2_db.tgz (ver. 2.0.1)")
        self.assertEqual(rh.get_md5('~/WORKSPACE/Robot@Home2_db.tgz'),
                         'c2a3536b6b98b907c56eda3a78300cbe')

        rh.logger.info("Computing MD5 hash value of Robot@Home2_files.tgz (ver. 2.0.1)")
        self.assertEqual(rh.get_md5('~/WORKSPACE/Robot@Home2_files.tgz'),
                         'c55465536738ec3470c75e1671bab5f2')

    def test_uncompress(self):
        """Testing untar(local_filename)

        Example:
            $ python -m unittest test_helpers.Test.test_uncompress
        """
        rh.logger.trace("*** Testing uncompress")
        rh.logger.info("Uncompressing ~/WORKSPACE/Robot@Home2_db.tgz")
        rh.uncompress('~/WORKSPACE/Robot@Home2_db.tgz', '~/WORKSPACE')
        # rh.logger.info("Uncompressing ~/WORKSPACE/Robot@Home2_files.tgz")
        # rh.uncompress('~/WORKSPACE/Robot@Home2_files.tgz', '~/WORKSPACE')

