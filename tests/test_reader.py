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
import pandas as pd    # Just to change default options as display.max_rows value
# import robotathome as rh
from robotathome import RobotAtHome, logger, set_log_level, log_levels, get_current_log_level, is_being_logged, flat2Dlist

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
        set_log_level('TRACE')

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
            self.rh_obj = RobotAtHome(rh_path = self.rh_path,
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
        del self.rh_obj

    def test_constructor_and_destructor(self):
        """
        Testing of RobotAtHome class constructor
        """
        # setUp method is the constructor
        # tearDown acts as the destructor
        pass

    def test_current_log_level(self):
        """
        Testing of RobotAtHome current_log_level function
        """
        logger.trace("*** Testing of current_log_level()")
        logger.info("Getting current log level")
        log_levels_key_no, log_levels_key_name = log_levels()
        logger.debug("get_log_levels (no): {}", log_levels_key_no)
        logger.debug("get_log_levels (name): {}", log_levels_key_name)
        level_no, level_name = get_current_log_level()
        logger.info("current log level (no): {}", level_no)
        logger.info("current log level (name): {}", level_name)
        logger.info("is_being_logged: {}", is_being_logged()) # default is_being_logged('DEBUG')

    # @logger.catch
    def test_get_con(self):
        """
        Testing of RobotAtHome.get_con()
        """
        con = self.rh_obj.get_con()
        logger.debug("con: {}", con)

    # @logger.catch
    def test_select_column(self):
        """
        Testing of RobotAtHome.select_column(column_name, table_name)
        """
        logger.trace("*** Testing of RobotAtHome.select_column(column_name, table_name)")
        logger.info("Extracting table names from the database")
        column = self.rh_obj.select_column('tbl_name', 'sqlite_master') # or sqlite_temp_master
        logger.info("\ncolumn (dataframe): {}", column)
        logger.debug("\ncolumn (numpy records): \n{}", column.to_records())
        logger.debug("\ncolumn (numpy): \n{}", column.to_numpy()) # or column.values
        logger.debug("\ncolumn (nested list): \n{}", column.to_numpy().tolist()) # or column.values.tolist()
        self.assertEqual(len(column), 29) # notice: 30 in earlier versions
        logger.debug("Lenght of column list: {}", len(column))


    """
    Framework
    """

    def test_get_homes(self):
        """
        Testing of RobotAtHome.get_homes()
        """
        logger.trace("*** Testing of RobotAtHome.get_homes()")
        logger.info("Extracting data from rh_homes table")
        ans = self.rh_obj.get_homes()
        logger.info("\nHomes: \n{}", ans)
        logger.info("\nHomes: \n{}", ans['name'].to_list())
        self.assertEqual(ans['name'].to_list(),
                         ['alma', 'anto', 'pare', 'rx2', 'sarmis'])
        logger.debug("homes# : {}", len(ans))

    def test_get_home_sessions(self):
        """
        Testing of RobotAtHome.get_home_sessions()
        """
        logger.trace("*** Testing of RobotAtHome.get_home_sessions()")
        logger.info("Extracting data from rh_home_sessions table")
        ans = self.rh_obj.get_home_sessions()
        logger.info("\nHome sessions: \n{}", ans)
        logger.info("\nHome sessions: \n{}", ans['name'].tolist())
        self.assertEqual(ans['name'].tolist(),
                         ['alma-s1', 'anto-s1', 'pare-s1', 'rx2-s1',
                          'sarmis-s1', 'sarmis-s2', 'sarmis-s3'])
        logger.info("home sessions# : {}", len(ans))

    def test_get_rooms(self):
        """
        Testing of RobotAtHome.get_rooms()
        """
        logger.trace("*** Testing of RobotAtHome.get_rooms()")
        logger.info("Extracting data from rh_rooms table")
        ans = self.rh_obj.get_rooms()
        logger.info("\nRooms: \n{}", ans)
        self.assertEqual(ans['name'].tolist(),
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
        logger.info("rooms# : {}", len(ans))

    def test_get_room_types(self):
        """
        Testing of RobotAtHome.get_room_types()
        """
        logger.trace("*** Testing of RobotAtHome.get_room_types()")
        logger.info("Extracting data from rh_room_types table")
        ans = self.rh_obj.get_room_types()
        logger.info("\nRoom types: \n{}", ans)
        logger.info("\nRoom types: \n{}", ans['name'].tolist())
        self.assertEqual(ans['name'].tolist(),
                         ['bathroom', 'bedroom', 'fullhouse',
                          'kitchen', 'livingroom', 'masterroom',
                          'corridor', 'dressingroom', 'hall']
                         )
        logger.info("Room types# : {}", len(ans))

    def test_get_sensors(self):
        """
        Testing of RobotAtHome.get_sensors()
        """
        logger.trace("*** Testing of RobotAtHome.get_sensors()")
        logger.info("Extracting data from rh_sensors table")
        ans = self.rh_obj.get_sensors()
        logger.info("\nSensors: \n{}", ans)
        logger.info("\nSensors: \n{}", ans['name'].tolist())
        self.assertEqual(ans['name'].tolist(),
                         ['HOKUYO1', 'RGBD_1', 'RGBD_2',
                          'RGBD_3', 'RGBD_4'])
        logger.info("Sensors # : {}", len(ans))

    def test_get_sensor_types(self):
        """
        Testing of RobotAtHome.get_sensor_types()
        """
        logger.trace("*** Testing of RobotAtHome.get_sensor_types()")
        logger.info("Extracting data from rh_sensor_types table")
        ans = self.rh_obj.get_sensor_types()
        logger.info("\nSensor types: \n{}", ans)
        logger.info("\nSensor types: \n{}", ans['name'].tolist())
        self.assertEqual(ans['name'].tolist(),
                         ['LASER SCANNER', 'RGBD CAMERA'])
        logger.info("Sensors types# : {}", len(ans))

    def test_get_hometopo(self):
        """
        Testing of RobotAtHome.get_hometopo()
        """
        logger.trace("*** Testing of RobotAtHome.get_hometopo()")
        logger.info("Extracting data from rh_hometopo table")
        ans = self.rh_obj.get_hometopo()
        logger.info("\nHome topo relationships: \n{}", ans)
        logger.info("Home topo relationships# : {}", len(ans))

    def test_get_locators(self):
        """
        Testing of RobotAtHome.get_locators()
        """
        logger.trace("*** Testing of RobotAtHome.get_locators()")
        logger.info("Extracting main indexes (locators) from the database")
        df_table = self.rh_obj.get_locators()
        logger.info("\nlocators: {}", df_table)
        self.assertEqual(len(df_table), 81)
        logger.debug("Length (num of rows) of locators table: {}", len(df_table))


    """
    Captured data
    """
    def test_get_sensor_observations(self):
        """Testing of get_sensor_observations
        """
        logger.trace("*** Testing of RobotAtHome.get_sensor_observations()")
        logger.info("Extracting sensor data from the rh2_sensor_observations view")

        df_full = self.rh_obj.get_sensor_observations('full')
        df_discarded = self.rh_obj.get_sensor_observations('discarded')
        df_lblrgbd = self.rh_obj.get_sensor_observations('lblrgbd')
        df_lsrscan = self.rh_obj.get_sensor_observations('lsrscan')

        logger.info("# Full observations set: {}", len(df_full))
        self.assertEqual(len(df_full), 116418)
        logger.info("# Discarded observations set: {}", len(df_discarded))
        self.assertEqual(len(df_discarded), 44118)
        logger.info("# Labeled rgbd observations set: {}", len(df_lblrgbd))
        self.assertEqual(len(df_lblrgbd), 32937)
        logger.info("# Laser scan observations set: {}", len(df_lsrscan))
        self.assertEqual(len(df_lsrscan), 39363)


        logger.info("\ndata:\n{}", df_lsrscan.info())

    def test_id2name(self):
        """Testing of id2name
        """
        logger.trace("*** Testing of RobotAtHome.id2name()")
        logger.info("Extracting names from ids")
        id = 1
        logger.info("Room {}: {}", id, self.rh_obj.id2name(id,'r'))
        logger.info("Room type {}: {}", id, self.rh_obj.id2name(id,'rt'))
        logger.info("Home {}: {}", id, self.rh_obj.id2name(id,'h'))
        logger.info("Home session {}: {}", id, self.rh_obj.id2name(id,'hs'))
        logger.info("Sensor {}: {}", id, self.rh_obj.id2name(id,'s'))
        logger.info("Sensor type {}: {}", id, self.rh_obj.id2name(id,'st'))
    def test_name2id(self):
        """Testing of name2id
        """
        logger.trace("*** Testing of RobotAtHome.name2id()")
        logger.info("Extracting id from name")

        logger.info("Room {}: {}", 'alma_kitchen1', self.rh_obj.name2id('alma_kitchen1','r'))
        logger.info("Room type {}: {}", 'kitchen', self.rh_obj.name2id('kitchen','rt'))
        logger.info("Home {}: {}", 'sarmis', self.rh_obj.name2id('sarmis','h'))
        logger.info("Home session {}: {}", 'sarmis_s2', self.rh_obj.name2id('sarmis_s2','hs'))
        logger.info("Sensor {}: {}", 'RGBD_2', self.rh_obj.name2id('RGBD_2','s'))
        logger.info("Sensor type {}: {}", 'LASER', self.rh_obj.name2id('LASER','st'))


    """
    RGBD data
    """
    def test_get_RGBD_files(self):
        """Testing of get_RGBD_files
        """
        logger.trace("*** Testing of RobotAtHome.get_RGBD_files()")
        logger.info("Extracting RGBD files from ids")
        id = 100000 # 0 <= id < inf
        [rgb_f, d_f] = self.rh_obj.get_RGBD_files(id)
        logger.info("Sensor observation {} files\n RGB file   : {}\n Depth file : {}", id, rgb_f, d_f )

    def test_get_RGBD_labels(self):
        """Testing of get_RGBD_labels
        """
        logger.trace("*** Testing of RobotAtHome.get_RGBD_labels()")
        logger.info("Extracting RGBD labels from ids")
        id = 100000 # 100000 <= id < 200000
        labels = self.rh_obj.get_RGBD_labels(id, False)
        logger.info("\nlabels: \n{}", labels)
        labels = self.rh_obj.get_RGBD_labels(id)
        logger.info("\nlabels: \n{}", labels)


    """
    Laser Scanner data
    """
    def test_get_laser_scan(self):
        """Testing of get_laser_scan
        """
        logger.trace("*** Testing of RobotAtHome.get_laser_scan()")
        logger.info("Extracting a laser scan from id")
        id = 200000 # 0 <= id < inf
        lsrscan = self.rh_obj.get_laser_scan(id)
        logger.info("\nSensor observation {} Laser scan : \n{}", id, lsrscan)
        logger.info("\naperture {}, max_range {}, no_of_shots {}", lsrscan.aperture, lsrscan.max_range, lsrscan.no_of_shots )


    """
    Scenes
    """
    def test_get_scenes(self):
        """Testing of get_scenes
        """
        logger.trace("*** Testing of RobotAtHome.get_scenes()")
        logger.info("Getting scene files")
        scenes = self.rh_obj.get_scenes()
        logger.info("\nScenes: \n{}", scenes)
        logger.info("\nScenes: \n{}", scenes[(scenes.home_session_id==0) & (scenes.room_id==3)].scene_file)
        logger.info("\nScenes: \n{}", scenes.query('home_session_id==0 & room_id==3').scene_file)

        hs_id = self.rh_obj.name2id('alma-s1','hs')
        r_id  = self.rh_obj.name2id('alma_kitchen1','r')
        scene =  scenes.query(f'home_session_id=={hs_id} & room_id=={r_id}')
        logger.info("\nScene: \n{}", scene)

    def test_get_scene_labels(self):
        """Testing of get_scenes
        """
        logger.trace("*** Testing of RobotAtHome.get_labels()")
        logger.info("Getting scene lables")
        scenes = self.rh_obj.get_scenes()
        id = 0
        scene_labels = self.rh_obj.get_scene_labels(id,True)
        logger.info("\nScene labels: \n{}", scene_labels.info())
        logger.info("\nScene labels: \n{}", scene_labels.query('local_id==0').loc[0,:])


    """
    Observations
    """
    def test_get_observations(self):
        """Testing of get_observations
        """
        logger.trace("*** Testing of RobotAtHome.get_observations()")
        logger.info("Getting observations")
        observations = self.rh_obj.get_observations()
        logger.info("\nObservations: \n{}", observations.info())

    def test_get_objects(self):
        """Testing of get_objects
        """
        logger.trace("*** Testing of RobotAtHome.get_objects()")
        logger.info("Getting objects")
        objects = self.rh_obj.get_objects()
        logger.info("\nObjects: \n{}")
        objects.info()
        r_name = 'alma_kitchen1'
        r_id  = self.rh_obj.name2id(r_name,'r')
        objects_in_room = objects.query(f'room_id=={r_id}')
        logger.info("\nObjects in room {} (id:{}) : \n{}", r_name, r_id, objects_in_room)

    def test_get_objects_in_observation(self):
        """Testing of get_observation_objects
        """
        logger.trace("*** Testing of RobotAtHome.get_objects_in_observation()")
        logger.info("Getting objects per observation")
        id = 0
        objects_in_observation = self.rh_obj.get_objects_in_observation(id)
        objects_in_observation.info()
        logger.info("\nObjects in observation: \n{}", objects_in_observation['name'])

    def test_get_object_relations(self):
        """Testing of get_object_relations
        """
        logger.trace("*** Testing of RobotAtHome.get_object_relations()")
        logger.info("Getting object relations")
        object_relations = self.rh_obj.get_object_relations()
        object_relations.info()
        my_object_relations = self.rh_obj.get_object_relations(id=4)
        logger.info("\nMy object relations: \n{}", my_object_relations[['obj1_id', 'obj2_id']])


    """
    Stuff
    """

    def test_query(self):
        """
        Testing of RobotAtHome.query()
        """
        logger.trace("*** Testing of RobotAtHome.query()")
        logger.info("Execute a sql query over robotathome database and returns records as a dataframe or as sqlite rows\n")

        queries = ["select id, name from rh_homes", "./test_query.sql"]

        for query in queries:
            logger.info("\nquery: \n{}\n", query)

            logger.info("Get output as a dataframe (default)")
            df_rows = self.rh_obj.query(query)
            logger.info("\ndf_rows: \n{}", df_rows)

            logger.info("Convert the dataframe in rows and print each of them")
            rows = df_rows.to_records()
            logger.info("\nrows: \n{}", rows)
            for row in rows:
                logger.info(row)

            logger.info("Get output as sqlite rows and print each of them")
            rows = self.rh_obj.query(query, df=False)
            logger.info("\nrows: \n{}", rows)
            for row in rows:
                logger.info(row)

    def test_get_sensor_observation_files(self):
        """
        Testing of get_sensor_observation_files
        """
        logger.trace("*** Testing of RobotAtHome.get_sensor_observation_files()")
        logger.info("Extracting file names from sensor_observations")

        rows = self.rh_obj.get_sensor_observation_files('lblrgbd',
                                                        'anto-s1',
                                                        0,
                                                        'anto_livingroom1',
                                                        'RGBD_2')
        logger.info("\nrows: \n{}", rows)
        self.assertEqual(len(rows), 355)
        logger.debug("Number of returned rows: {}", len(rows))

    def test_get_labels_from_lblrgbd(self):
        """
        Testing of get_labels_from_lblrgbd
        """
        logger.trace("*** Testing of RobotAtHome.get_labels_from_lblrgbd()")
        logger.info("Getting labels for a lblrgbd sensor_observations")
        df_rows = self.rh_obj.get_labels_from_lblrgbd(100000)
        logger.info("\n{}", df_rows)
        self.assertEqual(df_rows.shape, (11, 5))
        logger.debug("Number of returned rows: {}", len(df_rows))

    def test_get_mask_from_lblrgbd(self):
        """
        Testing of get_maak_from_lblrgbd
        """
        logger.trace("*** Testing of RobotAtHome.get_mask_from_lbl_rgbd()")
        logger.info("Getting mask for a lblrgbd sensor observation")
        mask = self.rh_obj.get_mask_from_lblrgbd(100000)
        logger.info("mask height: {}", len(mask))
        logger.info("mask width : {}", len(mask[0]))
        self.assertListEqual([len(mask), len(mask[0])], [320, 244])

    def test_create_table_linking_observations_and_lblrgbd(self):
        """
        Testing create_table_linking_observations_and_lblrgbd
        """
        logger.trace("*** Testing of RobotAtHome.create_table_linking_observations_and_lblrgbd()")
        logger.info("Linking lblrgbd and observations")
        self.rh_obj.create_table_linking_observations_and_lblrgbd()


    def test_get_object_type_names(self):
        """
        Testing of RobotAtHome.get_object_type_names()
        """
        logger.trace("*** Testing of RobotAtHome.get_object_type_names()")
        logger.info("Extracting object type names from the database")
        column = self.rh_obj.get_object_type_names()
        logger.info("\ncolumn: {}", column)
        self.assertEqual(len(column), 183)
        logger.debug("Length of object type names list: {}", len(column))

    def test_get_sensor_data(self):
        """Testing of get_observation_data
        """
        logger.trace("*** Testing of RobotAtHome.get_sensor_data()")
        logger.info("Extracting sensor data from the corresponding tables")

        sensor_data_table_names = self.rh_obj.get_names_of_sensor_data_tables()
        logger.info("\nsensor data tables:\n{}", sensor_data_table_names)

        for table_name in sensor_data_table_names:
            df = self.rh_obj.get_sensor_data(table_name)
            logger.info("\ndata:\n{}", df.info())
            logger.info("\nrow #1:\n{}", df.loc[1].transpose())




if __name__ == '__main__':
    unittest.main()
