#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home Python API - Workbench """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/12/10"
__license__ = "MIT"

from robotathome.dataset import Dataset

def set_extra_data():

    # ================
    #   Sensor types
    # ================

    sensor_types_dict = {0: "LASER SCANNER", 1: "RGBD CAMERA"}

    # ================
    #     Sensors
    # ================

    sensors_list = [[0, 0, "LASER"],
                    [1, 1, "RGBD_1"],
                    [2, 1, "RGBD_2"],
                    [3, 1, "RGBD_3"],
                    [4, 1, "RGBD_4"]]
    sensors_dict_reversed = dict((x[2], x[0]) for x in sensors_list)

    return sensor_types_dict, sensors_list, sensors_dict_reversed


def lblrgbd(rhds, homes_dict_reversed, sensors_dict_reversed):
    # Labeled RGB-D data
    rhds.unit["lblrgbd"].load_data()

    print(rhds.unit["lblrgbd"])
    home_sessions = rhds.unit["lblrgbd"].home_sessions

    num_observations = 0
    num_rooms = 0
    sensor_observation_id = 0
    for home_session_id, home_session in enumerate(home_sessions,start=0):
        num_rooms += len(home_session.rooms)
        home_id = homes_dict_reversed[home_session.get_home_name()]-1
        for room_id, room in enumerate(home_session.rooms):
            num_observations += len(room.sensor_observations)
            # change room_id by autoincremental
            print(room_id, home_session_id, home_id, room.name, len(room.sensor_observations))
            for sensor_observation in room.sensor_observations:
                print(sensor_observation_id,  # sensor_observation.id repeats id range for each room
                      room_id,
                      home_session_id,
                      home_id,
                      sensor_observation.name,
                      sensors_dict_reversed[sensor_observation.name],
                      sensor_observation.sensor_pose_x,
                      sensor_observation.sensor_pose_y,
                      sensor_observation.sensor_pose_z,
                      sensor_observation.sensor_pose_pitch,
                      sensor_observation.sensor_pose_roll,
                      sensor_observation.time_stamp)
                      # str(sensor_observation.files[index[0]]))
                      # sensor_observation.path)
                print(sensor_observation.get_intensity_file())
                sensor_observation_id += 1
    print(num_observations)
    print(num_rooms)

def lsrscan(rhds):

    #  Laser scans
    rhds.unit["lsrscan"].load_data()

    print(rhds.unit["lsrscan"])
    home_sessions = rhds.unit["lsrscan"].home_sessions

    num_sensor_sessions = 0
    num_rooms = 0
    for home_session_id, home_session in enumerate(home_sessions,start=0):
        num_rooms += len(home_session.rooms)
        for room_id, room in enumerate(home_session.rooms):
            num_sensor_sessions += len(room.sensor_sessions)
            print(home_session_id, room_id, room.name, len(room.sensor_sessions))
    print(num_sensor_sessions)
    print(num_rooms)


def main():
    # rhds = Dataset("MyRobot@Home")
    rhds = Dataset("MyRobot@Home", autoload=False)

    sensor_types_dict, sensors_list, sensors_dict_reversed = set_extra_data()

    # Characterized elements
    rhds.unit["chelmnts"].load_data()
    homes = rhds.unit["chelmnts"].get_home_names()
    homes_dict = dict(enumerate(homes, start=1))
    homes_dict_reversed = dict(map(reversed, homes_dict.items()))

    lblrgbd(rhds, homes_dict_reversed, sensors_dict_reversed)
    # lsrscan(rhds)


    return 0

if __name__ == "__main__":
    main()




