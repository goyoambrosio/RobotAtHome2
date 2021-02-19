#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import sys
import robotathome as rh
# import tests


class Test(unittest.TestCase):
    ''' Test of get_sensor_observation_files '''

    # nittest.skip("testing skipping")
    def setUp(self):
        rh.log.enable_logger(sink=sys.stderr, level="TRACE")
        rh.logger.trace("*** Test.setUp")
        rh.logger.info("""
        Remember:
        python -m unittest <testModule>.<className>.<function_name>
        e.g.
        python -m unittest test_toolbox.Test.test_get_home_names
        """)


        # self.rh_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/Robot@Home_DataSet_v2.0.0/'
        # self.rgbd_path = os.path.join(self.rh_path, 'files/rgbd')
        # self.db_filename = 'rh.db'
        # self.wspc_path = '/media/goyo/WDGREEN2TB-A/Users/goyo/Documents/PhD2020/WORKSPACE'

        self.rh_path = '/home/goyo/goyo2/Robot@Home_DataSet_v2.0.0'
        self.rgbd_path = os.path.join(self.rh_path, 'files/rgbd')
        self.db_filename = 'rh.db'
        self.wspc_path = '/home/goyo/goyo2/WORKSPACE'

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
        column = self.rh_obj.select_column('tbl_name', 'sqlite_temp_master')
        self.assertEqual(len(column), 1)
        rh.logger.debug("Lenght of column list: {}", len(column))

    def test_get_home_session_names(self):
        """
        Testing of RobotAtHome.get_session_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_home_session_names()")
        rh.logger.info("Extracting home session names from the database")
        column = self.rh_obj.get_home_session_names()
        self.assertEqual(column,['alma-s1', 'anto-s1', 'pare-s1', 'rx2-s1',
                                 'sarmis-s1', 'sarmis-s2', 'sarmis-s3'])
        rh.logger.debug(column)

    def test_get_home_names(self):
        """
        Testing of RobotAtHome.get_home_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_home_names()")
        rh.logger.info("Extracting home names from the database")
        column = self.rh_obj.get_home_names()
        self.assertEqual(column, ['alma', 'anto', 'pare', 'rx2', 'sarmis'])
        rh.logger.debug(column)

    def test_get_room_names(self):
        """
        Testing of RobotAtHome.get_room_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_room_names()")
        rh.logger.info("Extracting room names from the database")
        column = self.rh_obj.get_room_names()
        self.assertEqual(column, ['alma_bathroom1', 'alma_bedroom1',
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

        rh.logger.debug(column)

    def test_get_room_type_names(self):
        """
        Testing of RobotAtHome.get_room_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_room_type_names()")
        rh.logger.info("Extracting room type names from the database")
        column = self.rh_obj.get_room_type_names()
        self.assertEqual(column, ['bathroom', 'bedroom', 'corridor',
                                  'dressingroom', 'fullhouse', 'hall',
                                  'kitchen', 'livingroom', 'masterroom'])
        rh.logger.debug(column)

    def test_get_sensor_names(self):
        """
        Testing of RobotAtHome.get_sensor_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_sensor_names()")
        rh.logger.info("Extracting sensor names from the database")
        column = self.rh_obj.get_sensor_names()
        self.assertEqual(column, ['HOKUYO1', 'RGBD_1', 'RGBD_2',
                                  'RGBD_3', 'RGBD_4'])
        rh.logger.debug(column)

    def test_get_sensor_type_names(self):
        """
        Testing of RobotAtHome.get_sensor_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_sensor_type_names()")
        rh.logger.info("Extracting sensor type names from the database")
        column = self.rh_obj.get_sensor_type_names()
        self.assertEqual(column, ['LASER SCANNER', 'RGBD CAMERA'])
        rh.logger.debug(column)

    def test_get_object_type_names(self):
        """
        Testing of RobotAtHome.get_object_type_names()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_object_type_names()")
        rh.logger.info("Extracting object type names from the database")
        column = self.rh_obj.get_object_type_names()
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

    def test_process_with_yolo(self):
        """
        Testing get_video_from_rgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.process_with_yolo()")
        rh.logger.info("Processing images from a room with yolo")
        self.rh_obj.process_with_yolo(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2'
        )

    def test_process_with_rcnn(self):
        """
        Testing get_video_from_rgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.process_with_rcnn()")
        rh.logger.info("Processing images from a room with rcnn")
        my_result = self.rh_obj.process_with_rcnn(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2'
        )


if __name__ == '__main__':
    unittest.main()
