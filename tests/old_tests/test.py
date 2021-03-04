#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home Python API """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/06/17"
__license__ = "GPLv3"

import cv2
from robotathome.dataset import Dataset


def rgbd():
    """ About rgbd data """

    global rhds
    tab = 4
    print(rhds.unit["rgbd"])
    home_sessions = rhds.unit["rgbd"].home_sessions
    #print(str(home_sessions).expandtabs(0))
    #for home_session in home_sessions:
    #    print(str(home_session.rooms).expandtabs(tab))
    #    for room in home_session.rooms:
    #        print(str(room.name).expandtabs(tab*2))
    print(home_sessions[0].name)
    print(home_sessions[0].rooms[0].name)
    print(home_sessions[0].rooms[0].folder_path)

    path = home_sessions[0].rooms[0].folder_path

    # print(home_sessions[0].rooms[0].sensor_observations)

    sensor = home_sessions[0].rooms[0].sensor_observations[926]

    files = sensor.load_files()
    intensity_file = sensor.get_intensity_file()
    depth_file = sensor.get_depth_file()
    print(files)
    print(intensity_file)
    print(depth_file)

    sensor.show_intensity_image()
    sensor.show_depth_image()
    print('Press a key to continue ...')
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def lblrgbd():
    """ About labelled rgbd data """
    global rhds
    tab = 4
    print(rhds.unit["lblrgbd"])
    home_sessions = rhds.unit["lblrgbd"].home_sessions
    #print(str(home_sessions).expandtabs(0))
    #for home_session in home_sessions:
    #    print(str(home_session.rooms).expandtabs(tab))
    #    for room in home_session.rooms:
    #        print(str(room.name).expandtabs(tab*2))
    print(home_sessions[0].name)
    print(home_sessions[0].rooms[0].name)
    print(home_sessions[0].rooms[0].folder_path)

    path = home_sessions[0].rooms[0].folder_path

    # print(home_sessions[0].rooms[0].sensor_observations)

    sensor = home_sessions[0].rooms[0].sensor_observations[0]

    files = sensor.load_files()
    intensity_file = sensor.get_intensity_file()
    depth_file = sensor.get_depth_file()
    labels_file = sensor.get_labels_file()
    print(files)
    print(intensity_file)
    print(depth_file)
    print(labels_file)

    labels = sensor.get_labels()
    print(labels)
    # print(labels.as_dict_name())
    #print(labels.as_dict_id())
    # mask = sensor.__get_mask()
    #label_mask = sensor.get_label_mask(10)

    sensor.show_intensity_image()
    # sensor.show_depth_image()
    # sensor.show_label_mask_image(10)
    print('Press a key to continue ...')
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def lsrscan():
    """ About laser scans """

    global rhds
    tab = 4
    print(rhds.unit["lsrscan"])
    home_sessions = rhds.unit["lsrscan"].home_sessions

    print(home_sessions[0].name)
    print(home_sessions[0].rooms[0].name)
    print(home_sessions[0].rooms[0].folder_path)
    print(home_sessions[0].rooms[0].sensor_sessions)

    path = home_sessions[0].rooms[0].folder_path

    sensor = home_sessions[0].rooms[0].sensor_sessions[0].sensor_observations[0]
    print(sensor)
    print(type(sensor))
    print(sensor.load_files())
    print(sensor.get_type())
    print(type(sensor))
    laser_scan = sensor.get_laser_scan()
    print(laser_scan)
    print(laser_scan.vector_of_scans)
    print(laser_scan.vector_of_valid_scans)


def raw():

    """ About raw data """
    global rhds
    """
    tab = 4
    print(rhds.unit["raw"])
    home_sessions = rhds.unit["raw"].home_sessions
    """
    """
    print(str(home_sessions).expandtabs(0))
    for home_session in home_sessions:
        print(str(home_session.rooms).expandtabs(tab))
        for room in home_session.rooms:
            print(str(room.name).expandtabs(tab*2))
    """

    print(home_sessions[0].name)
    print(home_sessions[0].rooms[0].name)
    print(home_sessions[0].rooms[0].folder_path)

    path = home_sessions[0].rooms[0].folder_path

    sensor = home_sessions[0].rooms[0].sensor_observations[0]
    print(sensor)
    print(type(sensor))
    print(sensor.load_files())
    print(sensor.get_type())
    print(type(sensor))
    laser_scan = sensor.get_laser_scan(path)
    print(laser_scan)
    #print(laser_scan.vector_of_scans)
    #print(laser_scan.vector_of_valid_scans)

    sensor = home_sessions[0].rooms[0].sensor_observations[24]

    files = sensor.load_files()
    intensity_file = sensor.get_intensity_file()
    depth_file = sensor.get_depth_file()
    print(files)
    print(intensity_file)
    print(depth_file)

    sensor.show_intensity_file()
    sensor.show_depth_file()

    input('Press <enter> to continue')


def chelmnts():
    """  About categories """

    global rhds
    """
    print(rhds.unit["chelmnts"])
    print(rhds.unit["chelmnts"].get_home_names())
    home_dict = rhds.unit["chelmnts"].get_category_home_sessions()
    reversed_home_dict = dict(map(reversed, home_dict.items()))
    print(home_dict)
    print(reversed_home_dict)
    print(rhds.unit["chelmnts"].get_category_rooms())
    print(rhds.unit["chelmnts"].get_category_objects())
    """

    """
    homes = rhds.unit["chelmnts"].home_sessions
    tab = 4
    for home in homes:
        print(str(home).expandtabs(0))
        for room in home.rooms:
            print(str(room).expandtabs(tab))
            for object in room.objects:
                print(str(object).expandtabs(tab*2))
                print((str(object.features).expandtabs(tab*3)))
                print(object.features.as_dict())
            for relation in room.relations:
                print(str(relation).expandtabs(tab*2))
                print(str(relation.features).expandtabs(tab*3))
                print(relation.features.as_dict())
            for observation in room.observations:
                print(str(observation).expandtabs(tab*2))
                print(str(observation.features).expandtabs(tab*3))
                print(observation.features.as_dict())
                print(str(observation.scan_features).expandtabs(tab*3))
                print(observation.scan_features.as_dict())
    """

    """ About Home sessions, room, objects, relations and observations"""
    print('######## HOME #########')
    home_session = rhds.unit["chelmnts"].home_sessions[0]
    print(home_session)
    print(home_session.as_list())
    print(home_session.as_dict())

    print('######## HOMES #########')
    home_sessions = rhds.unit["chelmnts"].home_sessions
    print(home_sessions)
    print(home_sessions.get_ids())
    print(home_sessions.get_names())
    print(home_sessions.as_dict_id())
    print(home_sessions.as_dict_name())

    print('######## HOME.ROOM #########')
    room = home_sessions[0].rooms[0]
    print(room)
    print(room.as_list())
    print(room.as_dict())

    print('######## HOME.ROOMS #########')
    rooms = home_sessions[0].rooms
    print(rooms)
    print(rooms.get_ids())
    print(rooms.get_names())
    print(rooms.as_dict_name())
    print(rooms.as_dict_id())

    print('######## HOME.ROOM.OBJECT #########')
    object = home_sessions[0].rooms[0].objects[0]
    print(object)
    print(object.as_dict())

    print('######## HOME.ROOM.OBJECT.FEATURES #########')
    object_features = home_sessions[0].rooms[0].objects[0].features
    print(object_features)
    print(object_features.as_dict())

    print('######## HOME.ROOM.OBJECTS #########')
    objects = home_sessions[0].rooms[0].objects
    print(objects)
    print(objects.get_ids())
    print(objects.get_names())
    print(objects.as_dict_name())
    print(objects.as_dict_id())

    print('######## HOME.ROOM.RELATION #########')
    relation = home_sessions[0].rooms[0].relations[0]
    print(relation)
    print(relation.as_list())
    print(relation.as_dict())

    print('######## HOMES.ROOMS.RELATION.FEATURES #########')
    relation_features = home_sessions[0].rooms[0].relations[0].features
    print(relation_features)
    print(relation_features.as_dict())

    print('######## HOME.ROOM.RELATIONS #########')
    relations = home_sessions[0].rooms[0].relations
    print(relations)
    print(relations.get_ids())
    print(relations.get_obj1_ids())
    print(relations.get_obj2_ids())
    print(relations.as_dict_id())
    #print(relations.as_dict_obj1_id())
    #print(relations.as_dict_obj2_id())

    print('######## HOME.ROOM.OBSERVATION #########')
    observation = home_sessions[0].rooms[0].observations[0]
    print(observation)
    print(observation.as_list())
    print(observation.as_dict())

    print('######## HOME.ROOM.OBSERVATION.FEATURES #########')
    observation_features = home_sessions[0].rooms[0].observations[0].features
    print(observation_features)
    print(observation_features.as_dict())

    print('######## HOME.ROOM.OBSERVATION.SCAN_FEATURES #########')
    observation_scan_features = home_sessions[0].rooms[0].observations[0].scan_features
    print(observation_scan_features)
    print(observation_scan_features.as_dict())

    print('######## HOME.ROOM.OBSERVATIONS #########')
    observations = home_sessions[0].rooms[0].observations
    print(observations)
    print(observations.get_ids())
    print(observations.get_sensor_names())
    print(observations.as_dict_id())
    print(observations.as_dict_sensor_name())


def geomap():
    """ About 2d geometric maps """
    global rhds
    tab = 4
    print(rhds.unit["2dgeomap"])
    homes = rhds.unit["2dgeomap"].homes
    print(str(homes).expandtabs(0))
    for home in homes:
        print(str(home).expandtabs(0))
        # print(str(home.rooms).expandtabs(tab*1))
        for room in home.rooms:
            print(str(room).expandtabs(tab*1))
            print('        number of points: ' + str(len(room.points)))
            #for point in room.points:
            #    print(str(point).expandtabs(tab*2))
    print(homes[0].rooms[0].points[0])


def hometopo():
    """ About Home Topologies """
    global rhds
    tab = 4
    print(rhds.unit["hometopo"])
    homes = rhds.unit["hometopo"].homes
    print(str(homes).expandtabs(0))
    for home in homes:
        print(str(home.topo_relations).expandtabs(1))
        for topo_relation in home.topo_relations:
            print(str(topo_relation).expandtabs(tab*2))
    print(homes[0])
    print(homes[0].topo_relations[0].room1_name)
    print(homes[0].topo_relations[0].room2_name)
    print(homes[0].topo_relations[0].as_dict())
    print(homes[0].topo_relations.as_dict())
    print(homes[0].as_dict())
    print(homes.as_dict())


def main():
    """
    Multiline comment
    """

    # http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html#downloads
    # /media/goyo/WDGREEN2TB-A/Users/goyo/Documents

    global rhds

    rhds = Dataset("MyRobot@Home")

    """ About data units """
    """
    print(rhds)
    print(rhds["hometopo"].check_integrity(verbose=True))
    print(rhds["hometopo"].hash_for_directory())
    rhds["hometopo"].download()
    """

    rhds["lblscene"].download()


    print("That's all !!!")


if __name__ == "__main__":
    main()

