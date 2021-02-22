#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/22"
__license__ = "MIT"

import unittest
import os
import sys
import robotathome as rh
import pandas as pd
import numpy as np

# import tests


class Test(unittest.TestCase):
    ''' Test of get_sensor_observation_files '''

    # unittest.skip("testing skipping")
    def setUp(self):
        rh.log.enable_logger(sink=sys.stderr, level="DEBUG")
        rh.logger.trace("*** Test.setUp")
        rh.logger.info("""
        Remember:
        python -m unittest <testModule>.<className>.<function_name>
        e.g.
        python -m unittest test_toolbox.Test.test_get_home_names
        """)

        self.rh_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/Robot@Home_DataSet_v2.0.0/'
        self.rgbd_path = os.path.join(self.rh_path, 'files/rgbd')
        self.db_filename = 'rh.db'
        self.wspc_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/WORKSPACE'

        # self.rh_path = '/home/goyo/goyo2/Robot@Home_DataSet_v2.0.0'
        # self.rgbd_path = os.path.join(self.rh_path, 'files/rgbd')
        # self.db_filename = 'rh.db'
        # self.wspc_path = '/home/goyo/goyo2/WORKSPACE'

        self.rh_obj = rh.RobotAtHome(self.rh_path, self.wspc_path)

    def tearDown(self):
        rh.logger.trace("*** Test.tearDown")
        del self.rh_obj

    def test_constructor_and_destructor(self):
        """
        Testing of RobotAtHome class constructor
        """
        rh_obj = rh.RobotAtHome(self.rh_path, self.wspc_path)
        con = rh_obj.get_con()
        del rh_obj, con

    def test_current_log_level(self):
        """
        Testing of RobotAtHome current_log_level function
        """
        rh.logger.trace("*** Testing of current_log_level()")
        rh.logger.info("Getting current log level")
        log_levels_key_no, log_levels_key_name = rh.get_log_levels()
        rh.logger.debug("get_log_levels (no): {}", log_levels_key_no)
        rh.logger.debug("get_log_levels (name): {}", log_levels_key_name)
        level_no, level_name = rh.current_log_level()
        rh.logger.info("current log level (no): {}", level_no)
        rh.logger.info("current log level (name): {}", level_name)
        rh.logger.info("is_logged: {}", rh.is_logged()) # default rh.is_logged('DEBUG')

    def test_get_con(self):
        """
        Testing of RobotAtHome.get_con()
        """
        con = self.rh_obj.get_con()
        rh.logger.debug("con: {}", con)

    def test_select_column(self):
        """
        Testing of RobotAtHome.select_column(column_name, table_name)
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_column_names(column_name, table_name)")
        rh.logger.info("Extracting table names from the database")
        column = self.rh_obj.select_column('tbl_name', 'sqlite_master') # or sqlite_temp_master
        rh.logger.info("\ncolumn (dataframe): {}", column)
        rh.logger.debug("\ncolumn (numpy records): \n{}", column.to_records())
        rh.logger.debug("\ncolumn (numpy): \n{}", column.to_numpy()) # or column.values
        rh.logger.debug("\ncolumn (nested list): \n{}", column.to_numpy().tolist()) # or column.values.tolist()
        self.assertEqual(len(column), 30)
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_home_session_names(self):
        """
        Testing of RobotAtHome.get_session_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_home_session_names()")
        rh.logger.info("Extracting home session names from the database")
        column = self.rh_obj.get_home_session_names()
        rh.logger.info("\ncolumn: {}", column)
        rh.logger.debug("\ncolumn: {}", column.to_numpy().tolist())
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['alma-s1', 'anto-s1', 'pare-s1', 'rx2-s1',
                          'sarmis-s1', 'sarmis-s2', 'sarmis-s3'])
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_home_names(self):
        """
        Testing of RobotAtHome.get_home_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_home_names()")
        rh.logger.info("Extracting home names from the database")
        column = self.rh_obj.get_home_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['alma', 'anto', 'pare', 'rx2', 'sarmis'])
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_room_names(self):
        """
        Testing of RobotAtHome.get_room_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_room_names()")
        rh.logger.info("Extracting room names from the database")
        column = self.rh_obj.get_room_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['alma_bathroom1', 'alma_bedroom1',
                          'alma_fullhouse1', 'alma_kitchen1',
                          'alma_livingroom1', 'alma_masterroom1',
                          'anto_bathroom1', 'anto_bathroom2',
                          'anto_bedroom1', 'anto_bedroom2',
                          'anto_corridor1', 'anto_dressingroom1',
                          'anto_fullhouse1', 'anto_kitchen1',
                          'anto_livingroom1', 'anto_masterroom1',
                          'pare_bathroom1', 'pare_bathroom2',
                          'pare_bedroom1', 'pare_bedroom2',
                          'pare_corridor1', 'pare_fullhouse1',
                          'pare_hall1', 'pare_kitchen1',
                          'pare_livingroom1', 'pare_livingroom2',
                          'pare_masterroom1', 'rx2_bathroom1',
                          'rx2_bedroom1', 'rx2_fullhouse1',
                          'rx2_kitchen1', 'rx2_livingroom1',
                          'sarmis_bathroom1', 'sarmis_bathroom2',
                          'sarmis_bedroom1', 'sarmis_bedroom2',
                          'sarmis_bedroom3', 'sarmis_corridor1',
                          'sarmis_fullhouse1', 'sarmis_kitchen1',
                          'sarmis_livingroom1']
                         )
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_room_type_names(self):
        """
        Testing of RobotAtHome.get_room_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_room_type_names()")
        rh.logger.info("Extracting room type names from the database")
        column = self.rh_obj.get_room_type_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['bathroom', 'bedroom', 'corridor',
                          'dressingroom', 'fullhouse', 'hall',
                          'kitchen', 'livingroom', 'masterroom'])
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_sensor_names(self):
        """
        Testing of RobotAtHome.get_sensor_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_sensor_names()")
        rh.logger.info("Extracting sensor names from the database")
        column = self.rh_obj.get_sensor_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['HOKUYO1', 'RGBD_1', 'RGBD_2',
                          'RGBD_3', 'RGBD_4'])
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_sensor_type_names(self):
        """
        Testing of RobotAtHome.get_sensor_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_sensor_type_names()")
        rh.logger.info("Extracting sensor type names from the database")
        column = self.rh_obj.get_sensor_type_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(rh.flat2Dlist(column.to_numpy().tolist()),
                         ['LASER SCANNER', 'RGBD CAMERA'])
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_object_type_names(self):
        """
        Testing of RobotAtHome.get_object_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_object_type_names()")
        rh.logger.info("Extracting object type names from the database")
        column = self.rh_obj.get_object_type_names()
        rh.logger.info("\ncolumn: {}", column)
        self.assertEqual(len(column), 183)
        rh.logger.debug("Length of object type names list: {}", len(column))

    def test_get_sensor_observation_files(self):
        """
        Testing of get_sensor_observation_files
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_sensor_observation_files()")
        rh.logger.info("Extracting file names from sensor_observations")
        rows = self.rh_obj.get_sensor_observation_files('lblrgbd',
                                                        'anto-s1',
                                                        0,
                                                        'anto_livingroom1',
                                                        'RGBD_2')
        rh.logger.info("\nrows: \n{}", rows)
        self.assertEqual(len(rows), 355)
        rh.logger.debug("Number of returned rows: {}", len(rows))

    def test_get_video_from_rgbd(self):
        """
        Testing get_video_from_rgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_video_from_rgbd()")
        rh.logger.info("Making a video with images from a room")
        video_file_name = self.rh_obj.get_video_from_rgbd(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2'
        )

        video_file_size = os.path.getsize(
            os.path.join(self.wspc_path, video_file_name)
        )
        self.assertGreater(video_file_size, 6345000)
        rh.logger.debug("Video file name: {}", video_file_name)
        rh.logger.debug("Video file size: {}", video_file_size)

    def test_get_composed_video_from_lblrgbd(self):
        """
        Testing get_composed_video_from_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_composed_video_from_lblrgbd()")
        rh.logger.info("Making a composed video with 4 images per frame from a room")
        video_file_name = self.rh_obj.get_composed_video_from_lblrgbd(
            'anto-s1',
            0,
            'anto_livingroom1'
        )
        video_file_size = os.path.getsize(
            os.path.join(self.wspc_path, video_file_name)
        )
        self.assertGreater(video_file_size, 22273000)
        rh.logger.debug("Video file name: {}", video_file_name)
        rh.logger.debug("Video file size: {}", video_file_size)

    def test_get_labels_from_sensor_observation(self):
        """
        Testing of get_labels_from_sensor_observation
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_labels_from_sensor_observation()")
        rh.logger.info("Getting labels for a sensor_observations")
        df_rows = self.rh_obj.get_labels_from_sensor_observation(100000)
        rh.logger.info("\n{}", df_rows)
        self.assertEqual(df_rows.shape, (11, 5))
        rh.logger.debug("Number of returned rows: {}", len(df_rows))

    def test_get_mask_from_sensor_observation(self):
        """
        Testing of get_maak_from_sensor_observation
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_mask_from_sensor_observation()")
        rh.logger.info("Getting mask for a sensor observation")
        mask = self.rh_obj.get_mask_from_sensor_observation(100000)
        rh.logger.info("mask height: {}", len(mask))
        rh.logger.info("mask width : {}", len(mask[0]))
        self.assertListEqual([len(mask), len(mask[0])], [244, 320])

    def test_get_image_mask_from_label(self):
        """
        Testing of get_image_mask_from_label
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_image_mask_from_label()")
        rh.logger.info("Getting an mask image for a sensor observation label")
        mask = self.rh_obj.get_mask_from_sensor_observation(100000)
        img = self.rh_obj.get_image_mask_from_label(mask, 1)

        # from PIL import Image
        # Image.fromarray(img).show()
        # import cv2

        # cv2.imshow("Mask image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        rh.logger.debug("Number of non-zero pixels: {}", np.count_nonzero(img))
        self.assertEqual(np.count_nonzero(img), 6974)

        from matplotlib import pyplot as plt
        plt.imshow(img, cmap='Greys_r', interpolation='nearest')
        plt.show()

    def test_process_with_yolo(self):
        """
        Testing get_video_from_rgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.process_with_yolo()")
        rh.logger.info("Processing images from a room with yolo")
        detections, video_file_name = self.rh_obj.process_with_yolo(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2',
            # gpu=True
        )
        self.assertTupleEqual(detections.shape, (355, 3))
        video_file_size = os.path.getsize(
            os.path.join(self.wspc_path, video_file_name)
        )
        self.assertGreater(video_file_size, 7489000)


    def test_process_with_rcnn(self):
        """
        Testing get_video_from_rgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.process_with_rcnn()")
        rh.logger.info("Processing images from a room with rcnn")
        detections, video_file_name = self.rh_obj.process_with_rcnn(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2',
            # gpu=True

        )
        self.assertTupleEqual(detections.shape, (355, 3))
        video_file_size = os.path.getsize(
            os.path.join(self.wspc_path, video_file_name)
        )
        self.assertGreater(video_file_size, 7489000)



if __name__ == '__main__':
    unittest.main()
