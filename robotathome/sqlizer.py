#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home SQLizer """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/01/13"
__license__ = "MIT"


import os.path
import sys
import sqlite3
import re
import fire
from robotathome.dataset import Dataset


def dataset2sql(database_name='robotathome.db'):

    """ Docstring """

    # ===================
    #     Robot@Home
    # ===================

    rhds = Dataset("MyRobot@Home", autoload=False)

    # =====================
    #   SQLite initialize
    # =====================
    con = sql_connection(database_name)

    # =====================
    #    Filling tables
    # =====================
    fill_tables(con, rhds)

    # =====================
    #  Closing connections
    # =====================
    con.close()


def sql_connection(database_name):

    """ Docstring """

    try:

        # con = sqlite3.connect(':memory:')
        # print("Connection is established: Database is created in memory")
        con = sqlite3.connect(database_name)
        print("Connection is established: ", database_name)
        return con

    except NameError:

        print(NameError)


def create_tables(con, arg):

    """ Docstring """

    def create_tables_framework(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS sensors")
        cursor_obj.execute("CREATE TABLE sensors(id integer PRIMARY KEY, "
                           "sensor_type_id integer, "
                           "name text)")

        cursor_obj.execute("DROP TABLE IF EXISTS sensor_types")
        cursor_obj.execute("CREATE TABLE sensor_types(id integer PRIMARY KEY, "
                           "name text)")

        cursor_obj.execute("DROP TABLE IF EXISTS home_sessions")
        cursor_obj.execute("CREATE TABLE home_sessions("
                           "id integer PRIMARY KEY, "
                           "home_id integer, "
                           "name text)"
                           )

        cursor_obj.execute("DROP TABLE IF EXISTS homes")
        cursor_obj.execute("CREATE TABLE homes(id integer PRIMARY KEY, name text)")

        cursor_obj.execute("DROP TABLE IF EXISTS rooms")
        cursor_obj.execute("CREATE TABLE rooms("
                           "id integer PRIMARY KEY, "
                           "home_id integer, "
                           "name text, "
                           "room_type_id integer)"
                           )

        cursor_obj.execute("DROP TABLE IF EXISTS room_types")
        cursor_obj.execute("CREATE TABLE room_types(id integer PRIMARY KEY, "
                           "name text)")

        con.commit()

    def create_tables_chelmnts(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS object_types")
        cursor_obj.execute("CREATE TABLE object_types(id integer PRIMARY KEY, "
                           "name text)")

        cursor_obj.execute("DROP TABLE IF EXISTS objects")
        sql_str = ("CREATE TABLE objects("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "name text, "
                   "object_type_id integer, "
                   "planarity real, "
                   "scatter real, "
                   "linearity real, "
                   "min_height real, "
                   "max_height real, "
                   "centroid_x real, "
                   "centroid_y real, "
                   "centroid_z real, "
                   "volume real, "
                   "biggest_area real, "
                   "orientation real, "
                   "hue_mean real, "
                   "saturation_mean real, "
                   "value_mean real, "
                   "hue_stdv real, "
                   "saturation_stdv real, "
                   "value_stdv real, "
                   "hue_histogram_0 real, "
                   "hue_histogram_1 real, "
                   "hue_histogram_2 real, "
                   "hue_histogram_3 real, "
                   "hue_histogram_4 real, "
                   "value_histogram_0 real, "
                   "value_histogram_1 real, "
                   "value_histogram_2 real, "
                   "value_histogram_3 real, "
                   "value_histogram_4 real, "
                   "saturation_histogram_0 real, "
                   "saturation_histogram_1 real, "
                   "saturation_histogram_2 real, "
                   "saturation_histogram_3 real, "
                   "saturation_histogram_4 real)"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS relations")
        sql_str = ("CREATE TABLE relations("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "obj1_id integer, "
                   "obj2_id integer, "
                   "minimum_distance real, "
                   "perpendicularity real, "
                   "vertical_distance real, "
                   "volume_ratio real, "
                   "is_on integer, "
                   "abs_hue_stdv_diff real, "
                   "abs_saturation_stdv_diff real, "
                   "abs_value_stdv_diff real, "
                   "abs_hue_mean_diff real, "
                   "abs_saturation_mean_diff real, "
                   "abs_value_mean_diff real)"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS observations")
        sql_str = ("CREATE TABLE observations("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "sensor_id integer, "
                   "mean_hue real, "
                   "mean_saturation real, "
                   "mean_value real, "
                   "hue_stdv real, "
                   "saturation_stdv real, "
                   "value_stdv real, "
                   "hue_histogram_1 real, "
                   "hue_histogram_2 real, "
                   "hue_histogram_3 real, "
                   "hue_histogram_4 real, "
                   "hue_histogram_5 real, "
                   "saturation_histogram_1 real, "
                   "saturation_histogram_2 real, "
                   "saturation_histogram_3 real, "
                   "saturation_histogram_4 real, "
                   "saturation_histogram_5 real, "
                   "value_histogram_1 real, "
                   "value_histogram_2 real, "
                   "value_histogram_3 real, "
                   "value_histogram_4 real, "
                   "value_histogram_5 real, "
                   "distance real, "
                   "foot_print real, "
                   "volume real, "
                   "mean_mean_hue real, "
                   "mean_mean_saturation real, "
                   "mean_mean_value real, "
                   "mean_hue_stdv real, "
                   "mean_saturation_stdv real, "
                   "mean_value_stdv real, "
                   "mean_hue_histogram_1 real, "
                   "mean_hue_histogram_2 real, "
                   "mean_hue_histogram_3 real, "
                   "mean_hue_histogram_4 real, "
                   "mean_hue_histogram_5 real, "
                   "mean_saturation_histogram_1 real, "
                   "mean_saturation_histogram_2 real, "
                   "mean_saturation_histogram_3 real, "
                   "mean_saturation_histogram_4 real, "
                   "mean_saturation_histogram_5 real, "
                   "mean_value_histogram_1 real, "
                   "mean_value_histogram_2 real, "
                   "mean_value_histogram_3 real, "
                   "mean_value_histogram_4 real, "
                   "mean_value_histogram_5 real, "
                   "mean_distance real, "
                   "mean_foot_print real, "
                   "mean_volume real, "
                   "scan_area real, "
                   "scan_elongation real, "
                   "scan_mean_distance real, "
                   "scan_distance_stdv real, "
                   "scan_num_of_points integer, "
                   "scan_compactness real, "
                   "scan_compactness2 real, "
                   "scan_linearity real, "
                   "scan_scatter real)"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS objects_in_observation")
        cursor_obj.execute("CREATE TABLE objects_in_observation(id integer PRIMARY KEY, "
                           "observation_id integer, "
                           "object_id)")

        con.commit()

    def create_tables_raw(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS raw")
        sql_str = ("CREATE TABLE raw("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "name text, "
                   "sensor_id integer, "
                   "sensor_pose_x real, "
                   "sensor_pose_y real, "
                   "sensor_pose_z real, "
                   "sensor_pose_yaw real, "
                   "sensor_pose_pitch real, "
                   "sensor_pose_roll real, "
                   "laser_aperture real, "
                   "laser_max_range real, "
                   "laser_num_of_scans integer,"
                   "time_stamp integer, "
                   "sensor_type integer, "
                   "sensor_file_1 text, "
                   "sensor_file_2 text, "
                   "sensor_file_3 text, "
                   "files_path text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS raw_scans")
        sql_str = ("CREATE TABLE raw_scans("
                   "id integer PRIMARY KEY, "
                   "shot_id integer, "
                   "scan real, "
                   "valid_scan integer, "
                   "sensor_observation_id integer"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_rgbd(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS rgbd")
        sql_str = ("CREATE TABLE rgbd("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "name text, "
                   "sensor_id integer, "
                   "sensor_pose_x real, "
                   "sensor_pose_y real, "
                   "sensor_pose_z real, "
                   "sensor_pose_yaw real, "
                   "sensor_pose_pitch real, "
                   "sensor_pose_roll real, "
                   "laser_aperture real, "
                   "laser_max_range real, "
                   "laser_num_of_scans integer,"
                   "time_stamp integer, "
                   "sensor_type integer, "
                   "sensor_file_1 text, "
                   "sensor_file_2 text, "
                   "sensor_file_3 text, "
                   "files_path text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_lblrgbd(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS lblrgbd")
        sql_str = ("CREATE TABLE lblrgbd("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "name text, "
                   "sensor_id integer, "
                   "sensor_pose_x real, "
                   "sensor_pose_y real, "
                   "sensor_pose_z real, "
                   "sensor_pose_yaw real, "
                   "sensor_pose_pitch real, "
                   "sensor_pose_roll real, "
                   "laser_aperture real, "
                   "laser_max_range real, "
                   "laser_num_of_scans integer,"
                   "time_stamp integer, "
                   "sensor_type integer, "
                   "sensor_file_1 text, "
                   "sensor_file_2 text, "
                   "sensor_file_3 text, "
                   "files_path text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS lblrgbd_labels")
        sql_str = ("CREATE TABLE lblrgbd_labels("
                   "id integer PRIMARY KEY, "
                   "local_id integer, "
                   "name text, "
                   "sensor_observation_id integer, "
                   "object_type_id integer"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_lsrscan(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS lsrscan")
        sql_str = ("CREATE TABLE lsrscan("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "name text, "
                   "sensor_id integer, "
                   "sensor_pose_x real, "
                   "sensor_pose_y real, "
                   "sensor_pose_z real, "
                   "sensor_pose_yaw real, "
                   "sensor_pose_pitch real, "
                   "sensor_pose_roll real, "
                   "laser_aperture real, "
                   "laser_max_range real, "
                   "laser_num_of_scans integer,"
                   "time_stamp integer, "
                   "sensor_type integer, "
                   "sensor_file_1 text, "
                   "sensor_file_2 text, "
                   "sensor_file_3 text, "
                   "files_path text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        cursor_obj.execute("DROP TABLE IF EXISTS lsrscan_scans")
        sql_str = ("CREATE TABLE lsrscan_scans("
                   "id integer PRIMARY KEY, "
                   "shot_id integer, "
                   "scan real, "
                   "valid_scan integer, "
                   "sensor_observation_id integer"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_rctrscene(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS rctrscene")
        sql_str = ("CREATE TABLE rctrscene("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "scene_file text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_lblscene(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS lblscene")
        sql_str = ("CREATE TABLE lblscene("
                   "id integer PRIMARY KEY, "
                   "room_id integer, "
                   "home_session_id integer, "
                   "home_subsession_id integer, "
                   "home_id integer, "
                   "scene_file text"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)


        cursor_obj.execute("DROP TABLE IF EXISTS lblscene_bboxes")
        sql_str = ("CREATE TABLE lblscene_bboxes("
                   "id integer PRIMARY KEY, "
                   "local_id integer, "
                   "scene_id integer, "
                   "object_id integer, "
                   "object_name text, "
                   "bb_pose_x real, "
                   "bb_pose_y real, "
                   "bb_pose_z real, "
                   "bb_pose_yaw real, "
                   "bb_pose_pitch real, "
                   "bb_pose_roll real, "
                   "bb_corner1_x real, "
                   "bb_corner1_y real, "
                   "bb_corner1_z real, "
                   "bb_corner2_x real, "
                   "bb_corner2_y real, "
                   "bb_corner2_z real"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_2dgeomap(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS twodgeomap")
        sql_str = ("CREATE TABLE twodgeomap("
                   "id integer PRIMARY KEY, "
                   "home_id integer, "
                   "room_id integer, "
                   "x real, "
                   "y real, "
                   "z real"
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()

    def create_tables_hometopo(con):

        """ Docstring """

        cursor_obj = con.cursor()

        # Table creation

        cursor_obj.execute("DROP TABLE IF EXISTS hometopo")
        sql_str = ("CREATE TABLE hometopo("
                   "id integer PRIMARY KEY, "
                   "home_id integer, "
                   "room1_id integer, "
                   "room2_id integer "
                   ")"
                   )
        # print(sql_str)
        cursor_obj.execute(sql_str)

        con.commit()


    switcher = {
        "framework" : create_tables_framework,
        "chelmnts"  : create_tables_chelmnts,
        "raw"       : create_tables_raw,
        "rgbd"      : create_tables_rgbd,
        "lblrgbd"   : create_tables_lblrgbd,
        "lsrscan"   : create_tables_lsrscan,
        "rctrscene" : create_tables_rctrscene,
        "lblscene"  : create_tables_lblscene,
        "2dgeomap"  : create_tables_2dgeomap,
        "hometopo"  : create_tables_hometopo,
    }
    func = switcher.get(arg, lambda: "Invalid argument")
    func(con)


def fill_tables(con, rhds):

    """ Docstring """

    # inner global variables
    global sensors_dict_reversed
    global home_sessions_dict_reversed
    global homes_dict_reversed
    global room_types_dict_reversed
    global rooms_dict_reversed

    def fill_tables_framework_data():
        # =============================================================
        #                        FRAMEWORK_DATA
        # =============================================================

        # Set some needed tables with no explicit data
        dataunit_name = "raw"
        create_tables(con, "framework")
        # global sensors_dict_reversed
        if rhds.unit[dataunit_name].load_data():
            # sensor_types_dict, sensors_list, sensors_dict_reversed = set_framework_data(con, rhds)
            set_framework_data(con,
                               rhds.unit[dataunit_name])

    def fill_tables_chelmnts():
        # =============================================================
        #                           CHELMNTS
        # =============================================================

        dataunit_name = "chelmnts"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            chelmnts(con,
                     rhds.unit[dataunit_name])

    def fill_tables_raw():
        # =============================================================
        #                           RAW
        # =============================================================

        dataunit_name = "raw"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            num_of_observations = sensor_data(con,
                                              rhds.unit[dataunit_name],
                                              dataunit_name,
                                              "raw_scans")
            print("# stored observations : ", num_of_observations)

    def fill_tables_rgbd():
        # =============================================================
        #                           RGBD
        # =============================================================

        dataunit_name = "rgbd"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            num_of_observations = sensor_data(con,
                                              rhds.unit[dataunit_name],
                                              dataunit_name)
            print("# stored observations : ", num_of_observations)

    def fill_tables_lblrgbd():
        # =============================================================
        #                         LBLRGBD
        # =============================================================

        dataunit_name = "lblrgbd"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            num_of_observations = sensor_data(con,
                                              rhds.unit[dataunit_name],
                                              dataunit_name,
                                              "lblrgbd_labels",
                                              100000)
            print("# stored observations : ", num_of_observations)

    def fill_tables_lsrscan():
        # =============================================================
        #                         LSRSCAN
        # =============================================================

        dataunit_name = "lsrscan"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            num_of_observations = sensor_data(con,
                                              rhds.unit[dataunit_name],
                                              dataunit_name,
                                              "lsrscan_scans",
                                              200000)
            print("# stored observations : ", num_of_observations)

    def fill_tables_rctrscene():
        # =============================================================
        #                           RTRSCENE
        # =============================================================

        dataunit_name = "rctrscene"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            scene_data(con,
                       rhds.unit[dataunit_name],
                       dataunit_name
                       )
    def fill_tables_lblscene():
        # =============================================================
        #                           LBLSCENE
        # =============================================================

        dataunit_name = "lblscene"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            scene_data(con,
                       rhds.unit[dataunit_name],
                       dataunit_name
                       )

    def fill_tables_twodgeomap():
        # =============================================================
        #                          2DGEOMAP
        # =============================================================

        dataunit_name = "2dgeomap"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            twodgeomap(con,
                       rhds.unit[dataunit_name]
                       )

    def fill_tables_hometopo():
        # =============================================================
        #                        HOMETOPO
        # =============================================================

        dataunit_name = "hometopo"
        create_tables(con, dataunit_name)
        if rhds.unit[dataunit_name].load_data():
            hometopo(con,
                     rhds.unit[dataunit_name]
                     )

    fill_tables_framework_data()
    #fill_tables_chelmnts()
    #fill_tables_raw()
    #fill_tables_rgbd()
    #fill_tables_lblrgbd()
    #fill_tables_lsrscan()
    #fill_tables_rctrscene()
    #fill_tables_lblscene()
    #fill_tables_twodgeomap()
    fill_tables_hometopo()

    print("Tables successfully populated !")


def set_framework_data(con, dataunit):

    """ Docstring """

    global object_types_dict_reversed
    global sensor_types_dict #, sensors_list
    global sensors_dict_reversed
    global home_sessions_dict_reversed
    global homes_dict_reversed
    global room_types_dict_reversed
    global rooms_dict_reversed

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # ================
    #   Sensor types
    # ================

    sensor_types_dict = {0: "LASER SCANNER", 1: "RGBD CAMERA"}
    cursor_obj.executemany("INSERT INTO sensor_types VALUES(?, ?)",
                           sensor_types_dict.items())

    # ================
    #     Sensors
    # ================

    sensors_list = [[0, 0, "HOKUYO1"],
                    [1, 1, "RGBD_1"],
                    [2, 1, "RGBD_2"],
                    [3, 1, "RGBD_3"],
                    [4, 1, "RGBD_4"]]
    cursor_obj.executemany("INSERT INTO sensors VALUES(?, ?, ?)", sensors_list)
    sensors_dict_reversed = dict((x[2], x[0]) for x in sensors_list)

    # ============================================================
    #                        FRAMEWORK
    # ============================================================

    home_sessions = dataunit.home_sessions

    # =======================================
    #               HOMES
    # =======================================
    homes = []
    # get home names list from session names
    for home_session in home_sessions:
        homes.append(home_session.name.split("-s")[0])
    # remove duplicates
    homes = list(dict.fromkeys(homes))
    homes_dict = dict(enumerate(homes, start=0))
    homes_dict_reversed = dict(map(reversed, homes_dict.items()))
    # print(homes_dict_reversed)
    cursor_obj.executemany("INSERT INTO homes VALUES(?,?)",
                           list(enumerate(homes, start=0)))

    con.commit()

    # ======================================
    #            HOME_SESSIONS
    # ======================================
    sql_str = ("INSERT INTO home_sessions(id, home_id, name)"
               "VALUES(?, ?, ?)")
    home_session_id = 0
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        cursor_obj.execute(sql_str,
                           (home_session_id, home_id, home_session.name)
                           )
        home_session_id += 1
    home_sessions_dict = dict(enumerate(home_sessions.get_names(), start=0))
    home_sessions_dict_reversed = dict(map(reversed, home_sessions_dict.items()))

    con.commit()

    # ======================================
    #               ROOM_TYPES
    # ======================================

    room_types = []
    for home_session in home_sessions:
        for room in home_session.rooms:
            room_types.append(re.split('\d+', room.name)[0])
    room_types = list(dict.fromkeys(room_types))
    room_types_dict = dict(enumerate(room_types, start=0))
    room_types_dict_reversed = dict(map(reversed, room_types_dict.items()))
    # print(room_types)
    cursor_obj.executemany("INSERT INTO room_types VALUES(?,?)",
                           list(enumerate(room_types, start=0)))
    con.commit()

    # ======================================
    #                ROOMS
    # ======================================
    # print(homes_dict_reversed)
    # print(home_sessions_dict_reversed)
    # print(room_types_dict_reversed)

    sql_str = ("INSERT INTO rooms(id, home_id,"
               "                  name, room_type_id)"
               "VALUES(?, ?, ?, ?)")
    room_id = 0
    rooms = []
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        home_session_id = home_sessions_dict_reversed[home_session.name]
        for room in home_session.rooms:
            room_name = re.split('_\d+', room.name)[0]
            # print(room_name)
            room_type_id = room_types_dict_reversed[re.split('\d+', room.name)[0]]
            # print(home_id, home_session_id, room_type_id, room_name)
            # room_type_id = room_types_dict_reversed[re.split('\d+', room.name)[0]]
            # print(home_id, home_session_id, room_type_id, room.name)
            if home_session.get_home_name() + "_" + room_name not in rooms:
                cursor_obj.execute(sql_str,
                                   (room_id,
                                    # home_session_id,
                                    home_id,
                                    home_session.get_home_name() + "_" + room_name,
                                    # room.name,
                                    room_type_id)
                                   )
                rooms.append(home_session.get_home_name() + "_" + room_name)
                # rooms.append(home_session.get_home_name() + "_" + room.name)
                room_id += 1
    rooms = list(dict.fromkeys(rooms))
    rooms_dict = dict(enumerate(rooms, start=0))
    rooms_dict_reversed = dict(map(reversed, rooms_dict.items()))
    # print(rooms_dict_reversed)

    con.commit()


def chelmnts(con, dataunit):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # =============================================================
    #                           CHELMNTS
    # =============================================================

    global object_types_dict_reversed
    global sensors_dict_reversed
    global home_sessions_dict_reversed
    global homes_dict_reversed
    global room_types_dict_reversed
    global rooms_dict_reversed

    # ================
    #    Object types
    # ================

    object_types_dict = dataunit.get_category_objects()
    cursor_obj.executemany("INSERT INTO object_types VALUES(?,?)",
                           object_types_dict.items())
    con.commit()

    object_types_dict_reversed = dict(map(reversed, object_types_dict.items()))
    # print(object_types_dict)
    # print(object_types_dict_reversed)

    # ===============
    #  Home Sessions
    # ===============

    home_sessions = dataunit.home_sessions
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        home_session_id = home_sessions_dict_reversed[home_session.name]
        for room in home_session.rooms:
            # print(home_session.get_home_name(), home_session.name, room.name.split('_')[0])
            # print(home_session.get_home_name(), home_session.name, room.name)
            # room_id = rooms_dict_reversed[home_session.get_home_name() + "_" + room.name]
            room_id = rooms_dict_reversed[home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]]
            if len(room.name.split('_')) > 1:
                home_subsession_id = int(room.name.split('_')[1])-1
            else:
                home_subsession_id = 0

            # ===============
            #     Objects
            # ===============
            for object in room.objects:
                # print(home_id, home_session_id, home_subsession_id, room_id, object.id, object.name, object.type_id)
                # print(object.features)
                sql_str = "INSERT INTO objects(\
                                               id, \
                                               room_id, \
                                               home_id, \
                                               home_session_id,\
                                               home_subsession_id,\
                                               name, object_type_id, \
                                               planarity, \
                                               scatter, \
                                               linearity, \
                                               min_height, \
                                               max_height, \
                                               centroid_x, \
                                               centroid_y, \
                                               centroid_z, \
                                               volume, \
                                               biggest_area, \
                                               orientation, \
                                               hue_mean, \
                                               saturation_mean, \
                                               value_mean, \
                                               hue_stdv, \
                                               saturation_stdv, \
                                               value_stdv, \
                                               hue_histogram_0, \
                                               hue_histogram_1, \
                                               hue_histogram_2, \
                                               hue_histogram_3, \
                                               hue_histogram_4, \
                                               value_histogram_0, \
                                               value_histogram_1, \
                                               value_histogram_2, \
                                               value_histogram_3, \
                                               value_histogram_4, \
                                               saturation_histogram_0, \
                                               saturation_histogram_1, \
                                               saturation_histogram_2, \
                                               saturation_histogram_3, \
                                               saturation_histogram_4  \
                                               )  \
                                   VALUES(?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?)"
                cursor_obj.execute(sql_str,
                                   ([object.id,
                                     room_id,
                                     home_id,
                                     home_session_id,
                                     home_subsession_id,
                                     object.name,
                                     object.type_id] +
                                     object.features[0:32])
                                   )
                sys.stdout.write("\robject: %d" % (int(object.id)))

            # ===============
            #    Relations
            # ===============
            for relation in room.relations:
                sql_str = ("INSERT INTO relations("
                           "id, "
                           "room_id, "
                           "home_id, "
                           "home_session_id, "
                           "home_subsession_id, "
                           "obj1_id, obj2_id, "
                           "minimum_distance, "
                           "perpendicularity, "
                           "vertical_distance, "
                           "volume_ratio, "
                           "is_on, "
                           "abs_hue_stdv_diff, "
                           "abs_saturation_stdv_diff, "
                           "abs_value_stdv_diff, "
                           "abs_hue_mean_diff, "
                           "abs_saturation_mean_diff, "
                           "abs_value_mean_diff)"
                           "VALUES(?, ?, ?, ?, ?, ?, ?,"
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                           )
                cursor_obj.execute(sql_str,
                                   ([relation.id,
                                     room_id,
                                     home_id,
                                     home_session_id,
                                     home_subsession_id,
                                     relation.obj1_id,
                                     relation.obj2_id] +
                                     relation.features[0:11]
                                    )
                                   )
                #sys.stdout.write("\rrelation: %d" % (relation.id))

            # ===============
            #  Observations
            # ===============

            for observation in room.observations:
                sql_str = ("INSERT INTO observations("
                           "id, "
                           "room_id, "
                           "home_id, "
                           "home_session_id, "
                           "home_subsession_id, "
                           "sensor_id, "
                           "mean_hue, "
                           "mean_saturation, "
                           "mean_value, "
                           "hue_stdv, "
                           "saturation_stdv, "
                           "value_stdv, "
                           "hue_histogram_1, "
                           "hue_histogram_2, "
                           "hue_histogram_3, "
                           "hue_histogram_4, "
                           "hue_histogram_5, "
                           "saturation_histogram_1, "
                           "saturation_histogram_2, "
                           "saturation_histogram_3, "
                           "saturation_histogram_4, "
                           "saturation_histogram_5, "
                           "value_histogram_1, "
                           "value_histogram_2, "
                           "value_histogram_3, "
                           "value_histogram_4, "
                           "value_histogram_5, "
                           "distance, "
                           "foot_print, "
                           "volume, "
                           "mean_mean_hue, "
                           "mean_mean_saturation, "
                           "mean_mean_value, "
                           "mean_hue_stdv, "
                           "mean_saturation_stdv, "
                           "mean_value_stdv, "
                           "mean_hue_histogram_1, "
                           "mean_hue_histogram_2, "
                           "mean_hue_histogram_3, "
                           "mean_hue_histogram_4, "
                           "mean_hue_histogram_5, "
                           "mean_saturation_histogram_1, "
                           "mean_saturation_histogram_2, "
                           "mean_saturation_histogram_3, "
                           "mean_saturation_histogram_4, "
                           "mean_saturation_histogram_5, "
                           "mean_value_histogram_1, "
                           "mean_value_histogram_2, "
                           "mean_value_histogram_3, "
                           "mean_value_histogram_4, "
                           "mean_value_histogram_5, "
                           "mean_distance, "
                           "mean_foot_print, "
                           "mean_volume, "
                           "scan_area, "
                           "scan_elongation, "
                           "scan_mean_distance, "
                           "scan_distance_stdv, "
                           "scan_num_of_points, "
                           "scan_compactness, "
                           "scan_compactness2, "
                           "scan_linearity, "
                           "scan_scatter) "
                           "VALUES(?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?) "
                           )
                cursor_obj.execute(sql_str,
                                   ([observation.id,
                                     room_id,
                                     home_id,
                                     home_session.id,
                                     home_subsession_id,
                                     sensors_dict_reversed[observation.sensor_name]] +
                                    observation.features +
                                    observation.scan_features)
                                   )
                # print(observation.objects_id)
                objects_in_observation_list = zip(observation.objects_id,
                                  [observation.id]*len(observation.objects_id))
                # print(list(my_whatever))
                sql_str = ("INSERT INTO objects_in_observation("
                           "object_id, "
                           "observation_id) "
                           "VALUES(?, ?) "
                           )
                # Temporarily deactivate to get a faster development !!!!!!!!!
                cursor_obj.executemany(sql_str, objects_in_observation_list)



    con.commit()


def test():
    """ Docstring """

    return


def sensor_data(con,
                dataunit,
                dataunit_name,
                extra_data_table_name="extra_data",
                first_observation_id = 0):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    global object_types_dict_reversed
    global sensors_dict_reversed
    global home_sessions_dict_reversed
    global homes_dict_reversed
    global room_types_dict_reversed
    global rooms_dict_reversed

    home_sessions = dataunit.home_sessions

    # num_observations = 0
    # num_rooms = 0
    sensor_observation_id = first_observation_id
    label_id = 0
    scan_id = 0

    sql_str_sensor_observation = (
        "INSERT INTO " + dataunit_name + "("
        "id, "
        "room_id, "
        "home_session_id, "
        "home_subsession_id, "
        "home_id, "
        "name, "
        "sensor_id, "
        "sensor_pose_x, "
        "sensor_pose_y, "
        "sensor_pose_z, "
        "sensor_pose_yaw, "
        "sensor_pose_pitch, "
        "sensor_pose_roll, "
        "laser_aperture, "
        "laser_max_range, "
        "laser_num_of_scans, "
        "time_stamp, "
        "sensor_type, "
        "sensor_file_1, "
        "sensor_file_2, "
        "sensor_file_3, "
        "files_path"
        ") "
        "VALUES( ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
        )

    sql_str_labels = (
        "INSERT INTO " + extra_data_table_name + "("
        "id, "
        "local_id, "
        "name, "
        "sensor_observation_id, "
        "object_type_id"
        ") "
        "VALUES( ?, ?, ?, ?, ? )"
        )

    sql_str_scans = (
        "INSERT INTO " + extra_data_table_name + "("
        # "id, "
        "shot_id, "
        "scan, "
        "valid_scan, "
        "sensor_observation_id "
         ") "
        "VALUES( ?, ?, ?, ? )"
        )

    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        home_session_id = home_sessions_dict_reversed[home_session.name]

        for room in home_session.rooms:
            try:
                room_name = home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]
                room_id = rooms_dict_reversed[room_name]
                if len(room.name.split('_')) > 1:
                    home_subsession_id = int(room.name.split('_')[1])-1
                else:
                    home_subsession_id = 0
            except KeyError:
                try:
                    room_name = home_session.get_home_name() + "_" + re.split('_\D+', room.name)[0]
                    room_id = rooms_dict_reversed[room_name]
                    home_subsession_id = 0
                except KeyError:
                    print("********* KeyError: room " + room_name + " not found", "\n" )
                    continue

            # print(room.name, "|", room_name, "|", room_id, "|", home_session.name, "|", home_session_id, home_subsession_id)

            if dataunit.get_type() == "DatasetUnitLaserScans":
                num_of_sensor_sessions = len(room.sensor_sessions)
                for sensor_session in range(num_of_sensor_sessions):
                    # print("    ", "num_of_sensor_sessions: ", num_of_sensor_sessions, "sensor_session: ", sensor_session)
                    sensor_observations = room.sensor_sessions[sensor_session].sensor_observations
                    for sensor_observation in sensor_observations:
                        # break
                        sensor_observation.load_files()
                        cursor_obj.execute(sql_str_sensor_observation,
                                           (
                                               sensor_observation_id,
                                               room_id,
                                               home_session_id,
                                               sensor_session,
                                               home_id,
                                               sensor_observation.name,
                                               sensors_dict_reversed[sensor_observation.name],
                                               sensor_observation.sensor_pose_x,
                                               sensor_observation.sensor_pose_y,
                                               sensor_observation.sensor_pose_z,
                                               sensor_observation.sensor_pose_yaw,
                                               sensor_observation.sensor_pose_pitch,
                                               sensor_observation.sensor_pose_roll,
                                               4.1847,
                                               5.6,
                                               682,
                                               int(sensor_observation.time_stamp),
                                               0 if sensor_observation.get_type() == 'SensorLaserScanner' else 1,
                                               sensor_observation.files[0],
                                               sensor_observation.files[1] if (len(sensor_observation.files) > 1) else '',
                                               sensor_observation.files[2] if (len(sensor_observation.files) > 2) else '',
                                               os.path.relpath(sensor_observation.path)
                                           )
                                           )

                        laser_scan = sensor_observation.get_laser_scan()
                        for shot_id in range(0, len(laser_scan.vector_of_scans)-1):
                            cursor_obj.execute(sql_str_scans,
                                               (
                                                   # scan_id,
                                                   shot_id,
                                                   laser_scan.vector_of_scans[shot_id],
                                                   laser_scan.vector_of_valid_scans[shot_id],
                                                   sensor_observation_id
                                               )
                                               )
                            scan_id += 1

                        # print(os.path.relpath(sensor_observation.path))
                        # previous_time = int(sensor_observation.time_stamp)
                        sensor_observation_id += 1
                        sys.stdout.write("\rsensor_observation: %d" % (sensor_observation_id))
                    # print("\n")
            else:
                sensor_observations = room.sensor_observations
                for sensor_observation in sensor_observations:
                    # break
                    sensor_observation.load_files()
                    cursor_obj.execute(sql_str_sensor_observation,
                                       (
                                           sensor_observation_id,
                                           room_id,
                                           home_session_id,
                                           home_subsession_id,
                                           home_id,
                                           sensor_observation.name,
                                           sensors_dict_reversed[sensor_observation.name],
                                           sensor_observation.sensor_pose_x,
                                           sensor_observation.sensor_pose_y,
                                           sensor_observation.sensor_pose_z,
                                           sensor_observation.sensor_pose_yaw,
                                           sensor_observation.sensor_pose_pitch,
                                           sensor_observation.sensor_pose_roll,
                                           0,
                                           0,
                                           0,
                                           int(sensor_observation.time_stamp),
                                           0 if sensor_observation.get_type() == 'SensorLaserScanner' else 1,
                                           sensor_observation.files[0],
                                           sensor_observation.files[1] if (len(sensor_observation.files) > 1) else '',
                                           sensor_observation.files[2] if (len(sensor_observation.files) > 2) else '',
                                           os.path.relpath(sensor_observation.path)
                                       )
                                       )
                    if len(sensor_observation.files) > 2:
                        labels = sensor_observation.get_labels()
                        for label in labels:
                            try:
                                object_type_id = object_types_dict_reversed[re.split('_\d+', label.name)[0]]
                            except KeyError:
                                print("********* KeyError: object " + label.name + " not found", "\n" )
                                object_type_id = -1

                            cursor_obj.execute(sql_str_labels,
                                               (
                                                   label_id,
                                                   label.id,
                                                   label.name,
                                                   sensor_observation_id,
                                                   object_type_id
                                               )
                                               )
                            label_id += 1

                    if sensor_observation.get_type() == "SensorLaserScanner":
                        laser_scan = sensor_observation.get_laser_scan()
                        for shot_id in range(0, len(laser_scan.vector_of_scans)-1):
                            cursor_obj.execute(sql_str_scans,
                                               (
                                                   # scan_id,
                                                   shot_id,
                                                   laser_scan.vector_of_scans[shot_id],
                                                   laser_scan.vector_of_valid_scans[shot_id],
                                                   sensor_observation_id,
                                               )
                                               )
                            scan_id += 1

                    # print(os.path.relpath(sensor_observation.path))
                    # previous_time = int(sensor_observation.time_stamp)
                    sensor_observation_id += 1
                    sys.stdout.write("\rsensor_observation: %d" % (sensor_observation_id))
                # print("\n")
    print("\n")

    con.commit()

    cursor_obj.execute("DROP INDEX IF EXISTS " + "idx_" + dataunit_name + "_timestamp")
    sql_str = "create index idx_" + dataunit_name + "_timestamp on " + dataunit_name + "(time_stamp);"
    cursor_obj.execute(sql_str)

    con.commit()

    return sensor_observation_id


def scene_data(con,
               dataunit,
               dataunit_name):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # =============================================================
    #                         SCENE_DATA
    # =============================================================

    global object_types_dict_reversed
    global sensors_dict_reversed
    global home_sessions_dict_reversed
    global homes_dict_reversed
    global room_types_dict_reversed
    global rooms_dict_reversed

    scene_id = 0
    bb_id = 0

    sql_str_scene = (
        "INSERT INTO " + dataunit_name + "("
        "id, "
        "room_id, "
        "home_session_id, "
        "home_subsession_id, "
        "home_id, "
        "scene_file"
        ") "
        "VALUES( ?, ?, ?, ?, ?, ?)"
        )

    sql_str_bb = (
        "INSERT INTO " + dataunit_name + "_bboxes" + "("
        "id, "
        "local_id,"
        "scene_id, "
        "object_id, "
        "object_name, "
        "bb_pose_x, "
        "bb_pose_y, "
        "bb_pose_z, "
        "bb_pose_yaw, "
        "bb_pose_pitch, "
        "bb_pose_roll, "
        "bb_corner1_x, "
        "bb_corner1_y, "
        "bb_corner1_z, "
        "bb_corner2_x, "
        "bb_corner2_y, "
        "bb_corner2_z"
        ") "
        "VALUES( ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"
        )

    sql_str_select = (
        "SELECT id FROM objects WHERE "
        "room_id = ? AND "
        "home_id = ? AND "
        "home_session_id = ? AND "
        "home_subsession_id = ? AND "
        "name = ?"
    )


    home_sessions = dataunit.home_sessions
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        home_session_id = home_sessions_dict_reversed[home_session.name]
        for room in home_session.rooms:
            room_id = rooms_dict_reversed[home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]]
            if len(room.name.split('_')) > 1:
                home_subsession_id = int(room.name.split('_')[1])-1
            else:
                home_subsession_id = 0

            cursor_obj.execute(sql_str_scene,
                               (
                                   scene_id,
                                   room_id,
                                   home_session_id,
                                   home_subsession_id,
                                   home_id,
                                   room.scene_file
                                )
                               )
            # sys.stdout.write("\rscene: %d" % (scene_id))

            # ================================
            #     Bounding boxes (Objects)
            # ================================
            for bb in room.boundingboxes:
                cursor_obj.execute(sql_str_select,
                                   (
                                       room_id,
                                       home_id,
                                       home_session_id,
                                       home_subsession_id,
                                       bb.name
                                   )
                                   )
                row = cursor_obj.fetchone()
                if row is None:
                    object_id = None
                else:
                    object_id = row[0]
                cursor_obj.execute(sql_str_bb,
                                   (
                                       bb_id,
                                       bb.id,
                                       scene_id,
                                       object_id,
                                       bb.name,
                                       bb.bb_pose[0],
                                       bb.bb_pose[1],
                                       bb.bb_pose[2],
                                       bb.bb_pose[3],
                                       bb.bb_pose[4],
                                       bb.bb_pose[5],
                                       bb.bb_corner[0],
                                       bb.bb_corner[1],
                                       bb.bb_corner[2],
                                       bb.bb_corner[3],
                                       bb.bb_corner[4],
                                       bb.bb_corner[5],
                                    )
                                   )
                # sys.stdout.write("\rbounding box: %d" % (bb_id))
                bb_id += 1
            scene_id += 1

    con.commit()
    if bb_id > 0:
        print("scenes: %d, bounding boxes: %d" % (scene_id, bb_id))
    else:
        print("scenes: %d" % (scene_id))


def twodgeomap(con,
               dataunit):
    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # =============================================================
    #                          2DGEOMAP
    # =============================================================

    global homes_dict_reversed
    global rooms_dict_reversed

    point_id = 0

    sql_str_2dgeomap = (
        "INSERT INTO twodgeomap("
        "id, "
        "home_id, "
        "room_id, "
        "x, "
        "y, "
        "z "
        ") "
        "VALUES( ?, ?, ?, ?, ?, ?)"
        )

    homes = dataunit.homes
    for home in homes:
        home_id = homes_dict_reversed[home.name]
        for room in home.rooms:
            try:
                room_id = rooms_dict_reversed[home.name+"_"+room.name.split("_")[0]]
            except KeyError:
                continue
            for point in room.points:
                cursor_obj.execute(sql_str_2dgeomap,
                                   (
                                       point_id,
                                       home_id,
                                       room_id,
                                       point.x,
                                       point.y,
                                       point.z
                                    )
                                   )
                sys.stdout.write("\rpoint: %d" % (point_id))
                point_id += 1

    con.commit()

    print("\n")


def hometopo(con,
             dataunit):
    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # =============================================================
    #                          2DGEOMAP
    # =============================================================

    global homes_dict_reversed
    global rooms_dict_reversed

    topo_id = 0

    sql_str_hometopo = (
        "INSERT INTO hometopo("
        "id, "
        "home_id, "
        "room1_id, "
        "room2_id  "
        ") "
        "VALUES( ?, ?, ?, ?)"
        )

    homes = dataunit.homes
    for home in homes:
        home_id = homes_dict_reversed[home.name]
        for topo_relation in home.topo_relations:
            room1_id = rooms_dict_reversed[home.name+"_"+topo_relation.room1_name]
            room2_id = rooms_dict_reversed[home.name+"_"+topo_relation.room2_name]
            cursor_obj.execute(sql_str_hometopo,
                               (
                                   topo_id,
                                   home_id,
                                   room1_id,
                                   room2_id
                                )
                               )
            sys.stdout.write("\rpoint: %d" % (topo_id))
            topo_id += 1

    con.commit()

    print("\n")


def main():

    """ Docstring """

    fire.Fire(dataset2sql)
    # try:
    #     fire.Fire(dataset2sql)
    # except Exception as e:
    #     print("Oops! ", sys.exc_info()[0], " occurred.")
    #     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


    # main return
    return 0


if __name__ == "__main__":
    main()
