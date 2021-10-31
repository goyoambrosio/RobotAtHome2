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
import numpy as np
# from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import cv2
import imagehash
from PIL import Image
import gluoncv as gcv

class Test(unittest.TestCase):
    """Test class of toolbox module """

    # @unittest.skip("testing skipping")
    def setUp(self):
        """ The setUp() method allow you to define instructions that will be
                executed before and after each test method"""
        rh.log.enable_logger(sink=sys.stderr, level="TRACE")
        rh.logger.trace("*** Test.setUp")
        rh.logger.info("""
        Remember:
        python -m unittest <testModule>.<className>.<function_name>
        e.g.
        cd ~/Dropbox/GIT/RobotAtHome_API/tests
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
        """The tearDown() method allow you to define instructions that will be
               executed before each test method"""
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
        rh.logger.info("is_being_logged: {}", rh.is_being_logged()) # default rh.is_logged('DEBUG')

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

    def test_get_locators(self):
        """
        Testing of RobotAtHome.get_locators()
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_locators()")
        rh.logger.info("Extracting main indexes (locators) from the database")
        df_table = self.rh_obj.get_locators()
        rh.logger.info("\nlocators: {}", df_table)
        self.assertEqual(len(df_table), 81)
        rh.logger.debug("Length (num of rows) of locators table: {}", len(df_table))

    def test_query(self):
        """
        Testing of RobotAtHome.get_locators()
        """
        rh.logger.trace("*** Testing of RobotAtHome.query()")
        rh.logger.info("Execute a sql query over robotathome database and returns records as a dataframe or as sqlite rows\n")

        queries = ["select id, name from rh_homes", "./test_query.sql"]

        for query in queries:
            rh.logger.info("query: {}\n", query)

            rh.logger.info("Get result as a dataframe (default)")
            df_rows = self.rh_obj.query(query)
            rh.logger.info("df_rows: {}", df_rows)

            rh.logger.info("Convert the dataframe in rows and print each of them")
            rows = df_rows.to_records()
            rh.logger.info("rows: {}", rows)
            for row in rows:
                rh.logger.info(row)

            rh.logger.info("Get result as sqlite rows and print each of them")
            rows = self.rh_obj.query(query, df=False)
            rh.logger.info("rows: {}", rows)
            for row in rows:
                rh.logger.info(row)


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

    def test_get_labels_from_lblrgbd(self):
        """
        Testing of get_labels_from_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_labels_from_lblrgbd()")
        rh.logger.info("Getting labels for a lblrgbd sensor_observations")
        df_rows = self.rh_obj.get_labels_from_lblrgbd(100000)
        rh.logger.info("\n{}", df_rows)
        self.assertEqual(df_rows.shape, (11, 5))
        rh.logger.debug("Number of returned rows: {}", len(df_rows))

    def test_get_mask_from_lblrgbd(self):
        """
        Testing of get_maak_from_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_mask_from_lbl_rgbd()")
        rh.logger.info("Getting mask for a lblrgbd sensor observation")
        mask = self.rh_obj.get_mask_from_lblrgbd(100000)
        rh.logger.info("mask height: {}", len(mask))
        rh.logger.info("mask width : {}", len(mask[0]))
        self.assertListEqual([len(mask), len(mask[0])], [320, 244])

    def test_get_label_mask(self):
        """
        Testing of get_label_mask
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_label_mask()")
        rh.logger.info("Getting an mask image for a sensor observation label")
        mask = self.rh_obj.get_mask_from_lblrgbd(100000)
        img = self.rh_obj.get_label_mask(mask, [1])

        # from PIL import Image
        # Image.fromarray(img).show()

        # import cv2
        # cv2.imshow("Mask image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        rh.logger.debug("Image mask shape: {}", img[0].shape)
        rh.logger.debug("Number of non-zero pixels: {}", np.count_nonzero(img[0]))
        self.assertEqual(np.count_nonzero(img), 6974) # for sensor_observation_id: 100000

        plt.imshow(img[0], cmap='Greys_r', interpolation='nearest')
        plt.show()

    def test_get_rgb_image_from_lblrgbd(self):
        """
        Testing of get_rgb_image_from_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_rgb_image_from_lblrgbd()")
        rh.logger.info("Getting an intensity image (cv2) from labelled rgbd image set")
        img = self.rh_obj.get_rgb_image_from_lblrgbd(100000)

        rh.logger.debug("Image mask shape: {}", img.shape)
        rh.logger.debug("Image hash: {}", imagehash.dhash(Image.fromarray(img)))
        self.assertEqual(str(imagehash.dhash(Image.fromarray(img))), 'f030b0b0e0e033b3') # for sensor_observation_id: 100000

        # if rh.is_being_logged():
        #     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        #     plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        #     plt.show()

        if rh.is_being_logged():
            cv2.imshow('Debug mode (press any key to continue)', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def test_get_depth_image_from_lblrgbd(self):
        """
        Testing of get_depth_image_from_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.get_depth_image_from_lblrgbd()")
        rh.logger.info("Getting an depth image from labelled rgbd image set")
        img = self.rh_obj.get_depth_image_from_lblrgbd(100000)

        rh.logger.debug("Image mask shape: {}", img.shape)
        rh.logger.debug("Image hash: {}", imagehash.dhash(Image.fromarray(img)))
        self.assertEqual(str(imagehash.dhash(Image.fromarray(img))), '9eee6efebe9e9ccc') # for sensor_observation_id: 100000

        # if rh.is_being_logged():
        #     plt.imshow(img, cmap="gray")
        #     plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        #     plt.show()

        if rh.is_being_logged():
            cv2.imshow('Debug mode (press any key to continue)', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def test_lblrgbd_rgb_image_object_detection(self):
        """
        Testing of lblrgbd_rgb_image_object_detection
        """
        rh.logger.trace("*** Testing of RobotAtHome.lblrgbd_rgb_image_object_detection()")
        rh.logger.info("Object detection process over a labeled image")
        rh.logger.debug("available yolo_models: {}", rh.get_yolo_models())
        rh.logger.debug("available rcnn_models: {}", rh.get_rcnn_models())
        bgr_img, chw_img, class_names_, nn_out = self.rh_obj.lblrgbd_rgb_image_object_detection(100000,
                                                                                                'yolo3_darknet53_coco') # default
        [class_ids, scores, bounding_boxs] = nn_out

        df_nn_out = rh.nn_out2df(class_ids, scores, bounding_boxs)
        [df_class_ids, df_scores, df_bounding_boxs] = df_nn_out
        rh.logger.debug("df_nn_out: {}", df_nn_out)

        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        if rh.is_being_logged():
            gcv.utils.viz.plot_bbox(rgb_img,  # or chw_img,
                                    bounding_boxs[0],
                                    scores[0],
                                    class_ids[0],
                                    class_names=class_names_,
                                    thresh=0.2,
                                    linewidth=1
                                    )
            plt.show()

    def test_lblrgbd_object_detection(self):
        """
        Testing lblrgbd_object_detection
        """
        rh.logger.trace("*** Testing of RobotAtHome.lblrgbd_object_detection()")
        rh.logger.info("Object detection over a locator image set")
        detections, video_file_name = self.rh_obj.lblrgbd_object_detection(
            'lblrgbd',
            'anto-s1',
            0,
            'anto_livingroom1',
            'RGBD_2',
            model='faster_rcnn_resnet50_v1b_coco',
            # gpu=True
        )
        self.assertTupleEqual(detections.shape, (355, 3))
        video_file_size = os.path.getsize(
            os.path.join(self.wspc_path, video_file_name)
        )
        self.assertGreater(video_file_size, 7489000)

    def test_lblrgbd_plot_labels(self):
        """
        Testing lblrgbd_plot_labels
        """
        rh.logger.trace("*** Testing of RobotAtHome.lblrgbd_plot_labels()")
        rh.logger.info("Plot labels")
        img_id = 100000
        self.rh_obj.lblrgbd_plot_labels(img_id)


    @unittest.skip("testing skipping")
    def test_process_with_yolo(self):
        """
        Testing process_with_yolo
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

    @unittest.skip("testing skipping")
    def test_process_with_rcnn(self):
        """
        Testing process_with_rcnn
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

    def test_create_table_linking_observations_and_lblrgbd(self):
        """
        Testing create_table_linking_observations_and_lblrgbd
        """
        rh.logger.trace("*** Testing of RobotAtHome.create_table_linking_observations_and_lblrgbd()")
        rh.logger.info("Linking lblrgbd and observations")
        self.rh_obj.create_table_linking_observations_and_lblrgbd()



if __name__ == '__main__':
    unittest.main()
