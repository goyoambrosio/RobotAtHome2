#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home SQLizer """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/12/05"
__license__ = "MIT"


import sqlite3
from robotathome.dataset import Dataset

def sql_connection():

    try:

        # con = sqlite3.connect(':memory:')
        # print("Connection is established: Database is created in memory")
        con = sqlite3.connect('robotathome.db')
        print("Connection is established: robotathome.db")
        return con

    except NameError:

        print(NameError)


def create_tables(con):

    cursor_obj = con.cursor()

    # Table creation

    cursor_obj.execute("DROP TABLE IF EXISTS homes")
    cursor_obj.execute("CREATE TABLE homes(id integer PRIMARY KEY, name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS home_sessions")
    cursor_obj.execute("CREATE TABLE home_sessions("
                       "id integer PRIMARY KEY, "
                       "home_id integer, "
                       "name text)"
                       )

    cursor_obj.execute("DROP TABLE IF EXISTS room_types")
    cursor_obj.execute("CREATE TABLE room_types(id integer PRIMARY KEY, "
                       "name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS object_types")
    cursor_obj.execute("CREATE TABLE object_types(id integer PRIMARY KEY, "
                       "name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS sensors")
    cursor_obj.execute("CREATE TABLE sensors(id integer PRIMARY KEY, "
                       "sensor_type_id integer, "
                       "name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS sensor_types")
    cursor_obj.execute("CREATE TABLE sensor_types(id integer PRIMARY KEY, "
                       "name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS rooms")
    cursor_obj.execute("CREATE TABLE rooms("
                       "id integer PRIMARY KEY, "
                       "home_session_id integer, "
                       "home_id integer, "
                       "name text, "
                       "room_type_id integer)"
                       )

    cursor_obj.execute("DROP TABLE IF EXISTS objects")
    sql_str = ("CREATE TABLE objects("
               "id integer PRIMARY KEY, "
               "room_id integer, "
               "home_session_id integer, "
               "home_id integer, "
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
               "home_session_id integer, "
               "home_id integer, "
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
               "home_session_id integer, "
               "home_id integer, "
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

    cursor_obj.execute("DROP TABLE IF EXISTS raw")
    sql_str = ("CREATE TABLE observations("
               "id integer PRIMARY KEY, "
               "room_id integer, "
               "home_session_id integer, "
               "home_id integer, "
               "name text, "
               
               "scan_scatter real)"
               )
    # print(sql_str)
    cursor_obj.execute(sql_str)


    con.commit()


def set_extra_data(con):

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

    sensors_list = [[0, 0, "LASER"],
                    [1, 1, "RGBD_1"],
                    [2, 1, "RGBD_2"],
                    [3, 1, "RGBD_3"],
                    [4, 1, "RGBD_4"]]
    cursor_obj.executemany("INSERT INTO sensors VALUES(?, ?, ?)", sensors_list)
    sensors_dict_reversed = dict((x[2], x[0]) for x in sensors_list)

    return sensor_types_dict, sensors_list, sensors_dict_reversed

def main():

    # ===================
    #     Robot@Home
    # ===================

    # rhds = Dataset("MyRobot@Home")
    rhds = Dataset("MyRobot@Home", autoload=False)

    # Characterized elements
    rhds.unit["chelmnts"].load_data()
    # Labeled RGB-D data
    # rhds.unit["rgbd"].load_data()

    # =====================
    #   SQLite initialize
    # =====================
    con = sql_connection()

    # =====================
    #    Tables creation
    # =====================

    create_tables(con)

    # Set some needed tables with no explicit data
    # ============================================
    sensor_types_dict, sensors_list, sensors_dict_reversed = set_extra_data(con)

    # =====================
    #    Filling tables
    # =====================

    # Get a cursor to execute SQLite statements
    cursor_obj = con.cursor()

    # =============================================================
    #                           CHELMNTS
    # =============================================================

    # ================
    #      Homes
    # ================

    homes = rhds.unit["chelmnts"].get_home_names()
    # for home in homes:
    #     sql_str = "INSERT INTO homes(name) VALUES('" + home + "')"
    #     cursor_obj.execute(sql_str)

    # homes_dict = dict(enumerate(homes, start=1))
    # print(homes_dict.items())

    cursor_obj.executemany("INSERT INTO homes VALUES(?,?)",
                           list(enumerate(homes, start=0)))
    con.commit()

    # ================
    #    Room types
    # ================

    room_types = rhds.unit["chelmnts"].get_category_rooms()
    # print(room_types)
    cursor_obj.executemany("INSERT INTO room_types VALUES(?,?)",
                           room_types.items())
    # Adding ad-hoc values that appear 
    cursor_obj.execute("INSERT INTO room_types(id,name) VALUES(" +
                       str(len(room_types)) +
                       ",'dressingroom')")
    cursor_obj.execute("INSERT INTO room_types(id,name) VALUES(" +
                       str(len(room_types)+1) +
                       ",'fullhouse')")
    con.commit()

    # ================
    #    Object types
    # ================

    object_types = rhds.unit["chelmnts"].get_category_objects()
    cursor_obj.executemany("INSERT INTO object_types VALUES(?,?)",
                           object_types.items())
    con.commit()

    # ===============
    #  Home Sessions
    # ===============

    homes_dict = dict(enumerate(homes, start=1))
    # Two options for reversing a dictionary
    # homes_dict_reversed = {value: key for (key, value) in homes_dict.items()}
    homes_dict_reversed = dict(map(reversed, homes_dict.items()))
    # print(homes_dict_reversed)

    home_sessions = rhds.unit["chelmnts"].home_sessions
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]-1
        # print(home_id, home_session.id, home_session.name)
        sql_str = ("INSERT INTO home_sessions(id, home_id, name)"
                   "VALUES(?, ?, ?)")
        cursor_obj.execute(sql_str,
                           (home_session.id, home_id, home_session.name)
                           )
        # ===============
        #      Rooms
        # ===============
        for room in home_session.rooms:
            # print(room)
            # print(home_id, home_session.id, room.id, room.name, room.type_id)
            sql_str = ("INSERT INTO rooms(id, home_session_id, home_id,"
                       "                  name, room_type_id)"
                       "VALUES(?, ?, ?, ?, ?)")
            cursor_obj.execute(sql_str,
                               (room.id, home_session.id, home_id,
                                room.name, room.type_id)
                               )
            # ===============
            #     Objects
            # ===============
            for my_object in room.objects:
                # print(home_id, home_session.id, room.id, object.id, object.name, object.type_id)
                # print(object.features)
                sql_str = "INSERT INTO objects(id, room_id, home_session_id, home_id, \
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
                                   VALUES(?, ?, ?, ?, ?, ?,  \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                          ?, ?)"
                cursor_obj.execute(sql_str,
                                   ([my_object.id, room.id, home_session.id, home_id,
                                    my_object.name, my_object.type_id] +
                                    my_object.features[0:32])
                                   )
            # ===============
            #    Relations
            # ===============
            for relation in room.relations:
                # print(home_id, home_session.id, room.id, relation.id, relation.obj1_id, relation.obj2_id)
                # print(relation.features)
                sql_str = ("INSERT INTO relations(id, room_id, home_session_id, "
                           "home_id, "
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
                           "VALUES(?, ?, ?, ?, ?, ?,"
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                           )
                cursor_obj.execute(sql_str,
                                   ([relation.id, room.id, home_session.id, home_id,
                                    relation.obj1_id, relation.obj2_id] +
                                    relation.features[0:11])
                                   )
            # ===============
            #  Observations
            # ===============

            for observation in room.observations:
                # print(home_id, home_session.id, room.id, observation.id, observation.sensor_name)
                # print(observation.objects_id)
                # print(observation.features)
                # print(observation.scan_features)
                sql_str = ("INSERT INTO observations("
                           "id, "
                           "room_id, "
                           "home_session_id, "
                           "home_id, "
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
                           "VALUES(?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?) "
                           )
                cursor_obj.execute(sql_str,
                                   ([observation.id,
                                     room.id,
                                     home_session.id,
                                     home_id,
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

    # =============================================================
    #                           LBLRGBD
    # =============================================================




    con.commit()


    return 0


if __name__ == "__main__":
    main()
