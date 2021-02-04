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


# =========================
#      GLOBAL VARIABLES
# =========================
# Database connection
CON = 0
# Dataset
RHDS = None
# Reversed dictionaries
# (to avoid id queries as SELECT id ... WHERE name = ...)
OBJECT_TYPES_DICT_REVERSED = {}
SENSOR_TYPES_DICT = {}
SENSORS_DICT_REVERSED = {}
HOME_SESSIONS_DICT_REVERSED = {}
HOMES_DICT_REVERSED = {}
ROOM_TYPES_DICT_REVERSED = {}
ROOMS_DICT_REVERSED = {}

def dataset2sql(dataset_path='.', database_name='robotathome.db'):

    """ Docstring """

    global CON
    global RHDS

    # ===================
    #     Robot@Home
    # ===================

    # global RHDS
    RHDS = Dataset("MyRobot@Home", path=dataset_path, autoload=False)

    # =====================
    #   SQLite initialize
    # =====================

    # global database connection
    CON = sql_connection(database_name)

    # =====================
    #    Filling tables
    # =====================
    fill_tables()

    # =======================
    #  Executing sql scripts
    # =======================
    add_new_tables_and_views()

    # =====================
    #  Closing connections
    # =====================
    CON.close()


def sql_connection(database_name):

    """ Docstring """

    global CON

    try:
        CON = sqlite3.connect(database_name)
        print("Connection is established: ", database_name)
        return CON

    except NameError:

        print(NameError)


def run_sql_script(sql_file_name):

    """ Docstring """

    try:
        print("Running: ", sql_file_name)
        sql_file = open(sql_file_name)
        sql_as_string = sql_file.read()
        cursor_obj = CON.cursor()
        cursor_obj.executescript(sql_as_string)
    except Exception as e:
        print("Oops! ", sys.exc_info()[0], "occurred while running: ", sql_file_name)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


def create_tables(arg):

    """ Docstring """

    def create_tables_framework():

        """ Docstring """

        run_sql_script('create_tables_framework.sql')

    def create_tables_chelmnts():

        """ Docstring """

        run_sql_script('create_tables_chelmnts.sql')

    def create_tables_raw():

        """ Docstring """

        run_sql_script('create_tables_raw.sql')

    def create_tables_rgbd():

        """ Docstring """

        run_sql_script('create_tables_rgbd.sql')

    def create_tables_lblrgbd():

        """ Docstring """

        run_sql_script('create_tables_lblrgbd.sql')

    def create_tables_lsrscan():

        """ Docstring """

        run_sql_script('create_tables_lsrscan.sql')

    def create_tables_rctrscene():

        """ Docstring """

        run_sql_script('create_tables_rctrscene.sql')

    def create_tables_lblscene():

        """ Docstring """

        run_sql_script('create_tables_lblscene.sql')

    def create_tables_2dgeomap():

        """ Docstring """

        run_sql_script('create_tables_2dgeomap.sql')

    def create_tables_hometopo():

        """ Docstring """

        run_sql_script('create_tables_hometopo.sql')


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
    func()


def fill_tables():

    """ Docstring """

    def fill_tables_framework_data():
        # =============================================================
        #                        FRAMEWORK_DATA
        # =============================================================

        # Set some needed tables with no explicit data
        dataunit_name = "raw"
        create_tables("framework")
        if RHDS.unit[dataunit_name].load_data():
            set_framework_data(dataunit_name)

    def fill_tables_chelmnts():
        # =============================================================
        #                           CHELMNTS
        # =============================================================

        dataunit_name = "chelmnts"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            chelmnts(dataunit_name)

    def fill_tables_raw():
        # =============================================================
        #                           RAW
        # =============================================================

        dataunit_name = "raw"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            sensor_data(dataunit_name)

    def fill_tables_rgbd():
        # =============================================================
        #                           RGBD
        # =============================================================

        dataunit_name = "rgbd"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            sensor_data(dataunit_name)

    def fill_tables_lblrgbd():
        # =============================================================
        #                         LBLRGBD
        # =============================================================

        dataunit_name = "lblrgbd"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            sensor_data(dataunit_name, 100000)

    def fill_tables_lsrscan():
        # =============================================================
        #                         LSRSCAN
        # =============================================================

        dataunit_name = "lsrscan"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            sensor_data(dataunit_name, 200000)

    def fill_tables_rctrscene():
        # =============================================================
        #                           RTRSCENE
        # =============================================================

        dataunit_name = "rctrscene"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            scene_data(dataunit_name)

    def fill_tables_lblscene():
        # =============================================================
        #                           LBLSCENE
        # =============================================================

        dataunit_name = "lblscene"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            scene_data(dataunit_name)

    def fill_tables_twodgeomap():
        # =============================================================
        #                          2DGEOMAP
        # =============================================================

        dataunit_name = "2dgeomap"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            twodgeomap(dataunit_name)

    def fill_tables_hometopo():
        # =============================================================
        #                        HOMETOPO
        # =============================================================

        dataunit_name = "hometopo"
        create_tables(dataunit_name)
        if RHDS.unit[dataunit_name].load_data():
            hometopo(dataunit_name)

    fill_tables_framework_data()
    fill_tables_chelmnts()
    fill_tables_raw()
    fill_tables_rgbd()
    fill_tables_lblrgbd()
    fill_tables_lsrscan()
    fill_tables_rctrscene()
    fill_tables_lblscene()
    fill_tables_twodgeomap()
    fill_tables_hometopo()

    print("Tables successfully populated !")


def set_framework_data(dataunit_name):

    """ Docstring """

    global SENSOR_TYPES_DICT
    global SENSORS_DICT_REVERSED
    global HOME_SESSIONS_DICT_REVERSED
    global HOMES_DICT_REVERSED
    global ROOM_TYPES_DICT_REVERSED
    global ROOMS_DICT_REVERSED

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]

    # ================
    #   Sensor types
    # ================

    SENSOR_TYPES_DICT = {0: "LASER SCANNER", 1: "RGBD CAMERA"}
    cursor_obj.executemany("INSERT INTO rh_sensor_types VALUES(?, ?)",
                           SENSOR_TYPES_DICT.items())

    # ================
    #     Sensors
    # ================

    sensors_list = [[0, 0, "HOKUYO1"],
                    [1, 1, "RGBD_1"],
                    [2, 1, "RGBD_2"],
                    [3, 1, "RGBD_3"],
                    [4, 1, "RGBD_4"]]
    cursor_obj.executemany("INSERT INTO rh_sensors VALUES(?, ?, ?)", sensors_list)
    SENSORS_DICT_REVERSED = dict((x[2], x[0]) for x in sensors_list)

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
    HOMES_DICT_REVERSED = dict(map(reversed, homes_dict.items()))
    # print(HOMES_DICT_REVERSED)
    cursor_obj.executemany("INSERT INTO rh_homes VALUES(?,?)",
                           list(enumerate(homes, start=0)))

    CON.commit()

    # ======================================
    #            HOME_SESSIONS
    # ======================================
    sql_str = ("INSERT INTO rh_home_sessions(id, home_id, name)"
               "VALUES(?, ?, ?)")
    home_session_id = 0
    for home_session in home_sessions:
        home_id = HOMES_DICT_REVERSED[home_session.get_home_name()]
        cursor_obj.execute(sql_str,
                           (home_session_id, home_id, home_session.name)
                           )
        home_session_id += 1
    home_sessions_dict = dict(enumerate(home_sessions.get_names(), start=0))
    HOME_SESSIONS_DICT_REVERSED = dict(map(reversed, home_sessions_dict.items()))

    CON.commit()

    # ======================================
    #               ROOM_TYPES
    # ======================================

    room_types = []
    for home_session in home_sessions:
        for room in home_session.rooms:
            room_types.append(re.split('\d+', room.name)[0])
    room_types = list(dict.fromkeys(room_types))
    room_types_dict = dict(enumerate(room_types, start=0))
    ROOM_TYPES_DICT_REVERSED = dict(map(reversed, room_types_dict.items()))
    cursor_obj.executemany("INSERT INTO rh_room_types VALUES(?,?)",
                           list(enumerate(room_types, start=0)))
    CON.commit()

    # ======================================
    #                ROOMS
    # ======================================

    sql_str = ("INSERT INTO rh_rooms(id, home_id,"
               "                     name, room_type_id)"
               "VALUES(?, ?, ?, ?)")
    room_id = 0
    rooms = []
    for home_session in home_sessions:
        home_id = HOMES_DICT_REVERSED[home_session.get_home_name()]
        home_session_id = HOME_SESSIONS_DICT_REVERSED[home_session.name]
        for room in home_session.rooms:
            room_name = re.split('_\d+', room.name)[0]
            room_type_id = ROOM_TYPES_DICT_REVERSED[re.split('\d+', room.name)[0]]
            if home_session.get_home_name() + "_" + room_name not in rooms:
                cursor_obj.execute(sql_str,
                                   (room_id,
                                    home_id,
                                    home_session.get_home_name() + "_" + room_name,
                                    room_type_id)
                                   )
                rooms.append(home_session.get_home_name() + "_" + room_name)
                room_id += 1
    rooms = list(dict.fromkeys(rooms))
    rooms_dict = dict(enumerate(rooms, start=0))
    ROOMS_DICT_REVERSED = dict(map(reversed, rooms_dict.items()))

    print("\n")

    CON.commit()


def chelmnts(dataunit_name):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]

    # =============================================================
    #                           CHELMNTS
    # =============================================================

    global OBJECT_TYPES_DICT_REVERSED

    # ================
    #    Object types
    # ================

    object_types_dict = dataunit.get_category_objects()
    cursor_obj.executemany("INSERT INTO rh_object_types VALUES(?,?)",
                           object_types_dict.items())
    CON.commit()

    OBJECT_TYPES_DICT_REVERSED = dict(map(reversed, object_types_dict.items()))
    # print(object_types_dict)
    # print(OBJECT_TYPES_DICT_REVERSED)

    # ===============
    #  Home Sessions
    # ===============

    home_sessions = dataunit.home_sessions
    for home_session in home_sessions:
        home_id = HOMES_DICT_REVERSED[home_session.get_home_name()]
        home_session_id = HOME_SESSIONS_DICT_REVERSED[home_session.name]
        for room in home_session.rooms:
            # print(home_session.get_home_name(), home_session.name, room.name.split('_')[0])
            # print(home_session.get_home_name(), home_session.name, room.name)
            # room_id = ROOMS_DICT_REVERSED[home_session.get_home_name() + "_" + room.name]
            room_id = ROOMS_DICT_REVERSED[home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]]
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
                sql_str = "INSERT INTO rh_objects(\
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
                sql_str = ("INSERT INTO rh_relations("
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
                sql_str = ("INSERT INTO rh_observations("
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
                                     SENSORS_DICT_REVERSED[observation.sensor_name]] +
                                    observation.features +
                                    observation.scan_features)
                                   )
                # print(observation.objects_id)
                # remove repeated objects ids from the original data
                observation.objects_id = list(dict.fromkeys(observation.objects_id))
                objects_in_observation_list = zip(observation.objects_id,
                                  [observation.id]*len(observation.objects_id))
                # print(list(my_whatever))
                sql_str = ("INSERT INTO rh_objects_in_observation("
                           "object_id, "
                           "observation_id) "
                           "VALUES(?, ?) "
                           )
                # Temporarily deactivate to get a faster development !!!!!!!!!
                cursor_obj.executemany(sql_str, objects_in_observation_list)

    print("\n")

    CON.commit()


def test():
    """ Docstring """

    return


def sensor_data(dataunit_name, first_observation_id=0):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]

    home_sessions = dataunit.home_sessions

    # num_observations = 0
    # num_rooms = 0
    sensor_observation_id = first_observation_id
    label_id = 0
    scan_id = 0

    sql_str_sensor_observation = (
        "INSERT INTO rh_" + dataunit_name + "("
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
        "INSERT INTO rh_" + dataunit_name + "_labels " + "("
        "id, "
        "local_id, "
        "name, "
        "sensor_observation_id, "
        "object_type_id"
        ") "
        "VALUES( ?, ?, ?, ?, ? )"
        )

    sql_str_scans = (
        "INSERT INTO rh_" + dataunit_name + "_scans " + "("
        # "id, "
        "shot_id, "
        "scan, "
        "valid_scan, "
        "sensor_observation_id "
        ") "
        "VALUES( ?, ?, ?, ? )"
        )

    for home_session in home_sessions:
        home_id = HOMES_DICT_REVERSED[home_session.get_home_name()]
        home_session_id = HOME_SESSIONS_DICT_REVERSED[home_session.name]

        for room in home_session.rooms:
            try:
                room_name = home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]
                room_id = ROOMS_DICT_REVERSED[room_name]
                if len(room.name.split('_')) > 1:
                    home_subsession_id = int(room.name.split('_')[1])-1
                else:
                    home_subsession_id = 0
            except KeyError:
                try:
                    room_name = home_session.get_home_name() + "_" + re.split('_\D+', room.name)[0]
                    room_id = ROOMS_DICT_REVERSED[room_name]
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
                                               SENSORS_DICT_REVERSED[sensor_observation.name],
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
                                               sensor_observation.rel_path # os.path.relpath(sensor_observation.path)
                                           )
                                           )

                        laser_scan = sensor_observation.get_laser_scan()
                        for shot_id in range(0, len(laser_scan.vector_of_scans)):
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
                                           SENSORS_DICT_REVERSED[sensor_observation.name],
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
                                           sensor_observation.rel_path #os.path.relpath(sensor_observation.path)
                                       )
                                       )
                    if len(sensor_observation.files) > 2:
                        labels = sensor_observation.get_labels()
                        for label in labels:
                            try:
                                object_type_id = OBJECT_TYPES_DICT_REVERSED[re.split('_\d+', label.name)[0]]
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
                        for shot_id in range(0, len(laser_scan.vector_of_scans)):
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

    CON.commit()


def scene_data(dataunit_name):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]

    # =============================================================
    #                         SCENE_DATA
    # =============================================================

    scene_id = 0
    bb_id = 0

    sql_str_scene = (
        "INSERT INTO rh_" + dataunit_name + "("
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
        "INSERT INTO rh_" + dataunit_name + "_bboxes" + "("
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
        "SELECT id FROM rh_objects WHERE "
        "room_id = ? AND "
        "home_id = ? AND "
        "home_session_id = ? AND "
        "home_subsession_id = ? AND "
        "name = ?"
    )


    home_sessions = dataunit.home_sessions
    for home_session in home_sessions:
        home_id = HOMES_DICT_REVERSED[home_session.get_home_name()]
        home_session_id = HOME_SESSIONS_DICT_REVERSED[home_session.name]
        for room in home_session.rooms:
            room_id = ROOMS_DICT_REVERSED[home_session.get_home_name() + "_" + re.split('_\d+', room.name)[0]]
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


    if bb_id > 0:
        print("scenes: %d, bounding boxes: %d" % (scene_id, bb_id))
    else:
        print("scenes: %d" % (scene_id))

    print("\n")

    CON.commit()


def twodgeomap(dataunit_name):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]

    # =============================================================
    #                          2DGEOMAP
    # =============================================================

    point_id = 0

    sql_str_2dgeomap = (
        "INSERT INTO rh_twodgeomap("
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
        home_id = HOMES_DICT_REVERSED[home.name]
        for room in home.rooms:
            try:
                room_id = ROOMS_DICT_REVERSED[home.name+"_"+room.name.split("_")[0]]
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

    print("\n")

    CON.commit()


def hometopo(dataunit_name):

    """ Docstring """

    # Get a cursor to execute SQLite statements
    cursor_obj = CON.cursor()

    # Get the dataunit from global RHDS dataset
    dataunit = RHDS.unit[dataunit_name]


    # =============================================================
    #                          2DGEOMAP
    # =============================================================

    topo_id = 0

    sql_str_hometopo = (
        "INSERT INTO rh_hometopo("
        "id, "
        "home_id, "
        "room1_id, "
        "room2_id  "
        ") "
        "VALUES( ?, ?, ?, ?)"
        )

    homes = dataunit.homes
    for home in homes:
        home_id = HOMES_DICT_REVERSED[home.name]
        for topo_relation in home.topo_relations:
            room1_id = ROOMS_DICT_REVERSED[home.name+"_"+topo_relation.room1_name]
            room2_id = ROOMS_DICT_REVERSED[home.name+"_"+topo_relation.room2_name]
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

    print("\n")

    CON.commit()


def add_new_tables_and_views():

    """ Docstring """

    sql_file_names = ["create_view_sensor_observations.sql",
                      "create_view_scene_bb_objects.sql",
                      "create_new_rgbd_file_names.sql",
                      "create_new_scene_file_names.sql"]

    for sql_file_name in sql_file_names:
        run_sql_script(sql_file_name)


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
