#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home Python API """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/05/29"
__license__ = "GPLv3"

import fire
import os
import hashlib
import humanize
import wget
import ssl
# import requests
# import re


class Dataset():
    class Home():
        keys = ['id',
                'name',
                'rooms']

        def __init__(self, id, name, rooms):
            self.id = id
            self.name = name
            self.rooms = rooms

        def __str__(self):
            s = "\t" + str(self.id) + ", " + self.name + ", (" + \
                str(len(self.rooms)) + " rooms)"
            return s

        def __repr__(self):
            s = "<Home instance (" + str(self.id) + ":" + self.name + ")>"
            return s

        def as_list(self):
            return [self.id, self.name, self.rooms]

        def as_dict(self):
            new_dict = {
                'id': self.id,
                'name': self.name,
                'rooms': self.rooms
            }
            return new_dict

    class Homes(list):

        def __init__(self):
            pass

        def __str__(self):
            s = ''
            for item in self:
                s += str(item) + "\n"
            return s

        def __repr__(self):
            s = "<Home list instance (" + str(len(self)) + " items)>"
            return s

        def get_names(self):
            return [home.name for home in self]

        def get_ids(self):
            return [home.id for home in self]

        def as_dict_id(self):
            keys = [home.id for home in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_name(self):
            keys = [home.name for home in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class Room():
        def __init__(self, id, name,
                     type_id, type_name,
                     home_id,
                     objects, relations, observations):
            self.id = id
            self.name = name
            self.type_id = type_id
            self.type_name = type_name
            self.home_id = home_id
            self.objects = objects
            self.relations = relations
            self.observations = observations

        def __str__(self):
            s = "\t" + str(self.id) + ", " + self.name + ", " + \
                str(self.type_id) + ", " + self.type_name + ", " + \
                str(self.home_id) + ", (" + \
                str(len(self.objects)) + " objects), (" + \
                str(len(self.relations)) + " relations), (" + \
                str(len(self.observations)) + " observations)"
            return s

        def __repr__(self):
            s = "<Room instance (" + str(self.id) + ":" + self.name + ")>"
            return s

        def as_list(self):
            return [self.id,
                    self.name,
                    self.type_id,
                    self.type_name,
                    self.home_id,
                    self.objects,
                    self.relations,
                    self.observations]

        def as_dict(self):
            new_dict = {
                'id': self.id,
                'name': self.name,
                'type_id': self.type_id,
                'type_name': self.type_name,
                'home_id': self.home_id,
                'objects': self.objects,
                'relations': self.relations,
                'observations': self.observations
            }
            return new_dict

    class Rooms(list):

        def __init__(self):
            pass

        def __str__(self):
            s = ''
            for item in self:
                s += str(item) + "\n"
            return s

        def __repr__(self):
            s = "<Room list instance (" + str(len(self)) + " items)>"
            return s

        def get_names(self):
            return [room.name for room in self]

        def get_ids(self):
            return [room.id for room in self]

        def as_dict_id(self):
            keys = [room.id for room in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_name(self):
            keys = [room.name for room in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class Object():
        def __init__(self, id, name, type_id, type_name, room_id, features):
            self.id = id
            self.name = name
            self.type_id = type_id
            self.type_name = type_name
            self.room_id = room_id
            self.features = features

        def __str__(self):
            s = "\t" + str(self.id) + ", " + self.name + ", " + \
                str(self.type_id) + ", " + self.type_name + ", " + \
                str(self.room_id) + ", (" + \
                str(len(self.features)) + " features)"
            return s

        def __repr__(self):
            s = "<Object instance (" + str(self.id) + ":" + self.name + ")>"
            return s

        def as_list(self):
            return [self.id,
                    self.name,
                    self.type_id,
                    self.type_name,
                    self.room_id,
                    self.features]

        def as_dict(self):
            new_dict = {
                'id': self.id,
                'name': self.name,
                'type_id': self.type_id,
                'type_name': self.type_name,
                'room_id': self.room_id,
                'features': self.features
            }
            return new_dict

    class Objects(list):

        def __init__(self):
            pass

        def __str__(self):
            s = ''
            for item in self:
                s += str(item) + "\n"
            return s

        def __repr__(self):
            s = "<Objects list instance (" + str(len(self)) + " items)>"
            return s

        def get_names(self):
            return [object.name for object in self]

        def get_ids(self):
            return [object.id for object in self]

        def as_dict_id(self):
            keys = [object.id for object in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_name(self):
            keys = [object.name for object in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class ObjectFeatures(list):
        """
        The feature list follows this structure:
        0 : <planarity>
        1 : <scatter>
        2 : <linearity>
        3 : <min-height>
        4 : <max-height>
        5 : <centroid-x>
        6 : <centroid-y>
        7 : <centroid-z>
        8 : <volume>
        9 : <biggest-area>
        10 : <orientation>
        11 : <hue-mean>
        12 : <sturation-mean>
        13 : <vlue-mean>
        14 : <hue-stdv>
        15 : <saturation-stdv>
        16 : <value-stdv>
        17 : <hue-histogram(5)>
        18 : <hue-histogram(5)>
        19 : <hue-histogram(5)>
        20 : <hue-histogram(5)>
        21 : <hue-histogram(5)>
        22 : <value-histogram(5)>
        23 : <value-histogram(5)>
        24 : <value-histogram(5)>
        25 : <value-histogram(5)>
        26 : <value-histogram(5)>
        27 :<saturation-histogram(0)>
        28 :<saturation-histogram(1)>
        29 :<saturation-histogram(2)>
        30 :<saturation-histogram(3)>
        31 :<saturation-histogram(4)>
        """

        keys = ['planarity',
                'scatter',
                'linearity',
                'min-height',
                'max-height',
                'centroid-xyz',
                'volume',
                'biggest-area',
                'orientation',
                'hue-mean',
                'sturation-mean',
                'vlue-mean',
                'hue-stdv',
                'saturation-stdv',
                'value-stdv',
                'hue-histogram',
                'value-histogram',
                'saturation-histogram']

        def __init__(self):
            pass

        def __str__(self):
            s = "\t" + "planarity            : " + self[0] + "\n" + \
                "\t" + "scatter              : " + self[1] + "\n" + \
                "\t" + "linearity            : " + self[2] + "\n" + \
                "\t" + "min-height           : " + self[3] + "\n" + \
                "\t" + "max-height           : " + self[4] + "\n" + \
                "\t" + "centroid-xyz         : " + str(self[5:8]) + "\n" + \
                "\t" + "volume               : " + self[8] + "\n" + \
                "\t" + "biggest-area         : " + self[9] + "\n" + \
                "\t" + "orientation          : " + self[10] + "\n" + \
                "\t" + "hue-mean             : " + self[11] + "\n" + \
                "\t" + "saturation-mean      : " + self[12] + "\n" + \
                "\t" + "value-men            : " + self[13] + "\n" + \
                "\t" + "hue-stdy             : " + self[14] + "\n" + \
                "\t" + "saturation-stdy      : " + self[15] + "\n" + \
                "\t" + "value-stdy           : " + self[16] + "\n" + \
                "\t" + "hue-histogram        : " + str(self[17:22]) + "\n" + \
                "\t" + "value-histogram      : " + str(self[22:27]) + "\n" + \
                "\t" + "saturation-histogram : " + str(self[27:32])
            return s

        def __repr__(self):
            s = "<ObjectFeatures list instance (" + str(len(self)) + " items)>"
            return s

        def as_dict(self):
            new_list = self[0:5] + \
                       [self[5:8]] + \
                       self[8:17] + \
                       [self[17:22]] + [self[22:27]] + [self[27:]]

            zip_obj = zip(self.keys, new_list)
            new_dict = dict(zip_obj)
            return new_dict

    class ObjectRelation():
        def __init__(self, id,
                     obj1_id, obj1_name, obj1_type,
                     obj2_id, obj2_name, obj2_type,
                     features):
            self.id = id
            self.obj1_id = obj1_id
            self.obj1_name = obj1_name
            self.obj1_type = obj1_type
            self.obj2_id = obj2_id
            self.obj2_name = obj2_name
            self.obj2_type = obj2_type
            self.features = features

        def __str__(self):
            s = "\t" + self.id + ", " + \
                "(" + self.obj1_name + ", " + \
                self.obj1_id + ", " + \
                self.obj1_type + ")-" + \
                "(" + self.obj2_name + ", " + \
                self.obj2_id + ", " + \
                self.obj2_type + "), (" + \
                str(len(self.features)) + ") features"
            return s

        def __repr__(self):
            s = "<ObjectRelation instance (" + str(self.id) + ":" + \
                self.obj1_id + "-" + self.obj2_id + ")>"
            return s

        def as_list(self):
            return [self.id,
                    self.obj1_id,
                    self.obj1_name,
                    self.obj1_type,
                    self.obj2_id,
                    self.obj2_name,
                    self.obj2_type,
                    self.features]

        def as_dict(self):
            new_dict = {
                'id': self.id,
                'obj1_id': self.obj1_id,
                'obj1_name': self.obj1_name,
                'obj1_type': self.obj1_type,
                'obj2_id': self.obj2_id,
                'obj2_name': self.obj2_name,
                'obj2_type': self.obj2_type,
                'features': self.features
            }
            return new_dict

    class ObjectRelations(list):
        def __init__(self):
            pass

        def __str__(self):
            s = ''
            for item in self:
                s += str(item) + "\n"
            return s

        def __repr__(self):
            s = "<ObjectRelations list instance (" + str(len(self)) + \
                " items)>"
            return s

        def get_ids(self):
            return [relation.id for relation in self]

        def get_obj1_ids(self):
            return [relation.obj1_id for relation in self]

        def get_obj2_ids(self):
            return [relation.obj2_id for relation in self]

        def as_dict_id(self):
            keys = [relation.id for relation in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_obj1_id(self):
            keys = [relation.obj1_id for relation in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_obj2_id(self):
            keys = [relation.obj2_id for relation in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class ObjectRelationFeatures(list):
        """
        The feature list follows this structure:

        0 : <minimum-distance>
        1 : <perpendicularity>
        2 : <vertical-distance>
        3 : <volume-ratio>
        4 : <is-on>
        5 : <abs-hue-stdv-diff>
        6 : <abs-saturation-stdv-diff>
        7 : <abs-value-stdv-diff>
        8 : <abs-hue-mean-diff>
        9 : <abs-saturation-mean-diff>
        10 : <abs-value-mean-diff>
        """

        keys = ['minimum-distance',
                'perpendicularity',
                'vertical-distance',
                'volume-ratio',
                'is-on',
                'abs-hue-stdv-diff',
                'abs-saturation-stdv-diff',
                'abs-value-stdv-diff',
                'abs-hue-mean-diff',
                'abs-saturation-mean-diff',
                'abs-value-mean-diff']

        def __init__(self):
            pass

        def __str__(self):
            s = "\t" + "minimum-distance             : " + self[0] + "\n" + \
                "\t" + "perpendicularity             : " + self[1] + "\n" + \
                "\t" + "vertical-distance            : " + self[2] + "\n" + \
                "\t" + "volume-ratio                 : " + self[3] + "\n" + \
                "\t" + "is-on                        : " + self[4] + "\n" + \
                "\t" + "abs-hue-stdv-diff            : " + self[5] + "\n" + \
                "\t" + "abs-saturation-stdv-diff     : " + self[6] + "\n" + \
                "\t" + "abs-value-stdv-diff          : " + self[7] + "\n" + \
                "\t" + "abs-hue-mean-difforientation : " + self[8] + "\n" + \
                "\t" + "abs-saturation-mean-diff     : " + self[9] + "\n" + \
                "\t" + "abs-value-mean-diff          : " + self[10] + "\n"
            return s

        def __repr__(self):
            s = "<ObjectRelationFeatures list instance (" + str(len(self)) + \
                " items)>"
            return s

        def as_dict(self):
            zip_obj = zip(self.keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class Observation():
        def __init__(self,
                     id,
                     sensor_name,
                     objects_id,
                     features,
                     scan_features):
            self.id = id
            self.sensor_name = sensor_name
            self.objects_id = objects_id
            self.features = features
            self.scan_features = scan_features

        def __str__(self):
            s = "\t" + self.id + " : " + self.sensor_name + " : (" + \
                str(len(self.objects_id)) + \
                ") observed objects, (" + \
                str(len(self.features)) + \
                ") observation features, (" + \
                str(len(self.scan_features)) + \
                ") scan features"
            return s

        def __repr__(self):
            s = "<Observation instance (" + str(self.id) + ":" + \
                self.sensor_name + ")>"
            return s

        def as_list(self):
            return [self.id,
                    self.sensor_name,
                    self.objects_id,
                    self.features,
                    self.scan_features]

        def as_dict(self):
            new_dict = {
                'id': self.id,
                'sensor_name': self.sensor_name,
                'objects_id': self.objects_id,
                'features': self.features,
                'scan_features': self.scan_features
            }
            return new_dict

    class Observations(list):

        def __init__(self):
            pass

        def __str__(self):
            s = ''
            for item in self:
                s += str(item) + "\n"
            return s

        def __repr__(self):
            s = "<Observations list instance (" + str(len(self)) + \
                " items)>"
            return s

        def get_sensor_names(self):
            return [observation.sensor_name for observation in self]

        def get_ids(self):
            return [observation.id for observation in self]

        def as_dict_id(self):
            keys = [observation.id for observation in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

        def as_dict_sensor_name(self):
            keys = [observation.sensor_name for observation in self]
            zip_obj = zip(keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class ObservationFeatures(list):
        """
        The feature list follows this structure:
            0 : <mean-hue>
            1 : <mean-saturation>
            2 : <mean-value>
            3 : <hue-stdv>
            4 : <saturation-stdv>
            5 : <value-stdv>
         6:10 : <hue-histogram(5)>
        11:15 : <saturation-histogram(5)>
        16:20 : <value-histogram(5)>
           21 : <distance>
           22 : <foot-print>
           23 : <volume>
           24 : <mean-mean-hue>
           25 : <mean-mean-saturation>
           26 : <mean-mean-value>
           27 : <mean-hue-stdv>
           28 : <mean-saturation-stdv>
           29 : <mean-value-stdv>
        30:34 : <mean-hue-histogram(5)>
        35:39 : <mean-saturation-histogram(5)>
        40:44 : <mean-value-histogram(5)>
           45 : <mean-distance>
           46 : <mean-foot-print>
           47 : <mean-volume>
            0 : <area>
            1 : <elongation>
            2 : <mean-distance>
            3 : <distance-stdv>
            4 : <num-of-points>
            5 : <compactness>
            6 : <compactness2>
            7 : <linearity>
            8 : <scatter>
        """

        keys = ['mean-hue',
                'mean-saturation',
                'mean-value',
                'hue-stdv',
                'saturation-stdv',
                'value-stdv',
                'hue-histogram',
                'saturation-histogram',
                'value-histogram',
                'distance',
                'foot-print',
                'volume',
                'mean-mean-hue',
                'mean-mean-saturation',
                'mean-mean-value',
                'mean-hue-stdv',
                'mean-saturation-stdv',
                'mean-value-stdv',
                'mean-hue-histogram',
                'mean-saturation-histogram',
                'mean-value-histogram',
                'mean-distance',
                'mean-foot-print',
                'mean-volume']

        def __init__(self):
            pass

        def __str__(self):
            s = "\t" + "mean-hue                  : " + self[0] + "\n" + \
                "\t" + "mean-saturation           : " + self[1] + "\n" + \
                "\t" + "mean-value                : " + self[2] + "\n" + \
                "\t" + "hue-stdv                  : " + self[3] + "\n" + \
                "\t" + "saturation-stdv           : " + self[4] + "\n" + \
                "\t" + "value-stdv                : " + self[5] + "\n" + \
                "\t" + "hue-histogram             : " + str(self[6:11]) + "\n" + \
                "\t" + "saturation-histogram      : " + str(self[11:16]) + "\n" + \
                "\t" + "value-histogram           : " + str(self[16:21]) + "\n" + \
                "\t" + "distance                  : " + self[21] + "\n" + \
                "\t" + "foot-print                : " + self[22] + "\n" + \
                "\t" + "volume                    : " + self[23] + "\n" + \
                "\t" + "mean-mean-hue             : " + self[24] + "\n" + \
                "\t" + "mean-mean-saturation      : " + self[25] + "\n" + \
                "\t" + "mean-mean-value           : " + self[26] + "\n" + \
                "\t" + "mean-hue-stdv             : " + self[27] + "\n" + \
                "\t" + "mean-saturation-stdv      : " + self[28] + "\n" + \
                "\t" + "mean-value-stdv           : " + self[29] + "\n" + \
                "\t" + "mean-hue-histogram        : " + str(self[30:35]) + "\n" + \
                "\t" + "mean-saturation-histogram : " + str(self[35:40]) + "\n" + \
                "\t" + "mean-value-histogram      : " + str(self[40:45]) + "\n" + \
                "\t" + "mean-distance             : " + self[45] + "\n" + \
                "\t" + "mean-foot-print           : " + self[46] + "\n" + \
                "\t" + "mean-volume               : " + self[47] + "\n"
            return s

        def __repr__(self):
            s = "<ObservationFeatures list instance (" + \
                str(len(self)) + " items)>"
            return s

        def as_dict(self):
            new_list = self[0:6] + \
                       [self[6:11]] + [self[11:16]] + [self[16:21]] + \
                       self[21:30] + \
                       [self[30:35]] + [self[35:40]] + [self[40:45]] + \
                       self[45:]
            zip_obj = zip(self.keys, new_list)
            new_dict = dict(zip_obj)
            return new_dict

    class ObservationScanFeatures(list):
        """
        The feature list follows this structure:
            0 : <area>
            1 : <elongation>
            2 : <mean-distance>
            3 : <distance-stdv>
            4 : <num-of-points>
            5 : <compactness>
            6 : <compactness2>
            7 : <linearity>
            8 : <scatter>
        """
        keys = ['area',
                'elongation',
                'mean-distance',
                'distance-stdv',
                'num-of-points',
                'compactness',
                'compactness2',
                'linearity',
                'scatter']

        def __init__(self):
            pass

        def __str__(self):
            s = "\t" + "area          : " + self[0] + "\n" + \
                "\t" + "elongation    : " + self[1] + "\n" + \
                "\t" + "mean-distance : " + self[2] + "\n" + \
                "\t" + "distance-stdv : " + self[3] + "\n" + \
                "\t" + "num-of-points : " + self[4] + "\n" + \
                "\t" + "compactness   : " + self[5] + "\n" + \
                "\t" + "compactness2  : " + self[6] + "\n" + \
                "\t" + "linearity     : " + self[7] + "\n" + \
                "\t" + "scatter       : " + self[8]
            return s

        def __repr__(self):
            s = "<ObservationScanFeatures list instance (" + str(len(self)) + " items)>"
            return s

        def as_dict(self):
            zip_obj = zip(self.keys, self)
            new_dict = dict(zip_obj)
            return new_dict

    class DatasetUnit():

        """
        A plain text Robot@Home dataset
        """
        roar = "I'm a dataset"

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """
            Initializes the DatasetUnit with supplied values

            Attributes
            =========

            name : Human name of
            url  : url string to download it
            path : root path of
            expected_hash_code : the hash code the downloaded unit must have
            expected_size      : the number of bytes the downloaded copy must
                                 have
            """
            self.name = name
            self.url = url
            self.path = path
            self.expected_hash_code = expected_hash_code
            self.expected_size = expected_size

        def __repr__(self):
            return {'name': self.name, 'url': self.url}

        def __str__(self):
            s = '=' * len(self.name) + '\n' + \
                self.name + '\n' + \
                '=' * len(self.name) + '\n' + \
                '  url           = ' + self.url + '\n' + \
                '  path          = ' + self.path + '\n' + \
                '  expected hash = ' + self.expected_hash_code + '\n' + \
                '  expected size = ' + str(self.expected_size) + ' bytes  (' +\
                humanize.naturalsize(self.expected_size) + ')' + '\n'*2
            return s

        def check_folder_size(self, verbose=False):
            """
            Check that the expected size match with the real folder size
            verbose  : it outputs additional printed details
            """
            real_folder_size = self.size(self.path)
            if verbose:
                print('expected size : ' + str(self.expected_size) +
                      ' bytes (' +
                      humanize.naturalsize(self.expected_size) + ')')
                print('counted       : ' + str(real_folder_size) +
                      ' bytes (' +
                      humanize.naturalsize(real_folder_size) + ')')
            return self.expected_size == real_folder_size

        def check_integrity(self, in_depth=False, verbose=False):
            """
            It checks that:
            - self.path folder exist
            - the expected size match with the real size

            in_depth : for future, it will check the hash value
            verbose  : it outputs additional printed details
            """
            if verbose:
                print('Checking      : ' + self.name)
                print('folder        : ' + self.path)
            folder_exist = os.path.isdir(self.path)
            if verbose:
                print('folder exist  : ' + str(folder_exist))
            if folder_exist:
                correct_size = self.check_folder_size(verbose)
                if verbose:
                    print('correct size  : ' + str(correct_size))
            return folder_exist and correct_size

        def download(self):
            """ignore SSL certificate verification!"""
            ssl._create_default_https_context = ssl._create_unverified_context
            wget.download(self.url)

        def size(self, path, *, follow_symlinks=True):
            """
            https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
            """
            try:
                with os.scandir(path) as it:
                    return sum(self.size(entry,
                                         follow_symlinks=follow_symlinks)
                               for entry in it)
            except NotADirectoryError:
                return os.stat(path, follow_symlinks=follow_symlinks).st_size

        def hash_for_directory(self, hashfunc=hashlib.sha1):
            """
            Computes a single hash for a given folder. It works fine for
            small-sized files (e.g. a source tree or something, where every
            file individually can fit into RAM easily), ignoring empty
            directories.

            It works like this:

            1. Find all files in the directory recursively and sort them by
               name
            2. Calculate the hash (default: SHA-1) of every file (reads whole
               file into memory)
            3. Make a textual index with "filename=hash" lines
            4. Encode that index back into a UTF-8 byte string and hash that

            You can pass in a different hash function
            (https://docs.python.org/3/library/hashlib.html) as second
            parameter

            Source:
            https://stackoverflow.com/questions/545387/linux-compute-a-single-hash-for-a-given-folder-contents

            Other options:
            https://stackoverflow.com/questions/24937495/how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python

            """
            filenames = sorted(os.path.join(dp, fn)
                               for dp, _, fns in os.walk(self.path)
                               for fn in fns)
            index = '\n'.join('{}={}'.format(os.path.relpath(fn, self.path),
                                             hashfunc(open(fn, 'rb').read()).
                                             hexdigest()) for fn in filenames)
            return hashfunc(index.encode('utf-8')).hexdigest()

    class DatasetUnitCharacterizedElements(DatasetUnit):

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)
            self.__categories_file = "types.txt"
            self.__home_key_string = "home"
            self.__room_key_string = "room"
            self.__object_key_string = "object"
            self.categories = self.__load_categories()
            self.home_files = self.__get_home_files()
            self.homes = self.__load_home_files()

        def __str__(self):
            """ Categories """

            s = "\n"
            s += "Categories" + "\n" + "==========" + "\n"*2
            for category in self.categories:
                w = category + " (" + str(len(self.categories[category])) + ")"
                s += w + "\n"
                s += "-" * len(w) + "\n"
                for item in self.categories[category]:
                    s += item + ", " + self.categories[category][item] + "\n"
                s += "\n"
            return super().__str__() + s

        def __get_type(self):
            """
            Obsolete function. Just for reference.
            """
            file_name = "types.txt"
            searched_key = "N_homes"
            ignored_keys = ["N_typesOfRooms", "N_typesOfObjects"]
            types = {}

            with open(self.path+"/"+file_name, "r") as file_handler:
                # Lines are initially considered ignored
                keep_line = False
                # Read the first line
                line = file_handler.readline()
                """
                loop over lines:
                - if line contains the searched_key then keep next lines
                  until a newly ignored_key be found
                """
                while line:
                    if searched_key in line:
                        keep_line = True
                    else:
                        for ignored_key in ignored_keys:
                            if ignored_key in line:
                                keep_line = False
                        if keep_line:
                            words = line.strip().split()
                            types[words[0]] = words[1]

                    line = file_handler.readline()
            return types

        def __load_categories(self):
            """
            types.txt file contains information about homes, room categories
            and object categories that are considered.
            This function read  a file with those elements and return it as a
            dictionary:
                key   : Name of the category
                value : Dict with items belonging to the category:
                    key   : id
                    value : item's name
            """
            categories = {}

            with open(self.path+"/"+self.__categories_file, "r") as file_handler:
                # Initially they key is empty
                key = ""
                # Read the first line
                line = file_handler.readline()
                """
                First lines before a key is found are ignored
                """
                while line:
                    words = line.strip().split()
                    if words[0].isdigit():
                        if key:
                            categories[key][words[0]] = words[1]
                    else:
                        key = words[0]
                        categories[key] = {}
                    line = file_handler.readline()
            return categories

        def get_homes(self):
            for key in self.categories.keys():
                if self.__home_key_string in key.lower():
                    return self.categories[key]

        def get_rooms(self):
            for key in self.categories.keys():
                if self.__room_key_string in key.lower():
                    return self.categories[key]

        def get_objects(self):
            for key in self.categories.keys():
                if self.__object_key_string in key.lower():
                    return self.categories[key]

        def __get_home_files(self):
            """
            returns a dict with all files under homes folders in a dictionary:
            key   : home's name
            value : a list with files under key folder

            """
            home_file = {}
            home_list = list(self.get_homes().values())
            for home in home_list:
                home_file[home] = os.listdir(self.path + '/' + home)
            return home_file

        def __load_home_files(self):
            """
            """
            home_list = Dataset.Homes()
            home_dict = self.get_homes()
            reversed_home_dict = dict(map(reversed, home_dict.items()))

            for home_files_key, home_files_value in self.home_files.items():
                home_name = home_files_key
                home_id = int(reversed_home_dict[home_files_key])
                room_list = Dataset.Rooms()
                home = Dataset.Home(home_id, home_name, room_list)
                """
                Loop a file per room
                """
                for home_file_name in home_files_value:
                    path = self.path + "/" + home_files_key + "/" + \
                           home_file_name
                    # print(path)
                    with open(path, "r") as file_handler:
                        """
                        Read the first line with the following structure:
                        word  0: Home
                        word  1: <readable-home-id>
                        word  2: <home-id>
                        word  3: Room_type
                        word  4: <readable-room-type>
                        word  5: <room-type-id>
                        word  6: ID
                        word  7: <room-id>
                        word  8: N_objects
                        word  9: <number-of-objects>
                        word 10: N_objectFeatures
                        word 11: <number-of-object-features>
                        """
                        home_header = file_handler.readline()
                        words = home_header.strip().split()
                        # print(words)
                        room_id         = words[7]
                        """
                        File record does not contain a name for the room so
                        the type_name is given as name.
                        """
                        room_name       = words[4]
                        room_type_id    = int(words[5])
                        room_type_name  = words[4]
                        num_of_objects  = int(words[9])
                        num_of_features = int(words[11])
                        objects         = Dataset.Objects()
                        relations       = Dataset.ObjectRelations()
                        observations    = Dataset.Observations()
                        room = Dataset.Room(room_id, room_name,
                                            room_type_id, room_type_name,
                                            home_id,
                                            objects, relations, observations)
                        # Read the next num_of_objects lines
                        for object_index in range(num_of_objects):
                            """
                            Read a line with the following structure:
                            word  0 : <object-label>
                            word  1 : <object-ID>
                            word  2 : <object-type>
                            word  3 : <object-ground-truh>
                            word  4 : <planarity>
                            word  5 : <scatter>
                            word  6 : <linearity>
                            word  7 : <min-height>
                            word  8 : <max-height>
                            word  9 : <centroid-x>
                            word 10 : <centroid-y>
                            word 11 : <centroid-z>
                            word 12 : <volume>
                            word 13 : <biggest-area>
                            word 14 : <orientation>
                            word 15 : <hue-mean>
                            word 16 : <sturation-mean>
                            word 17 : <vlue-mean>
                            word 18 : <hue-stdv>
                            word 19 : <saturation-stdv>
                            word 20 : <value-stdv>
                            word 21 : <hue-histogram(5)>
                            word 22 : <hue-histogram(5)>
                            word 23 : <hue-histogram(5)>
                            word 24 : <hue-histogram(5)>
                            word 25 : <hue-histogram(5)>
                            word 26 : <value-histogram(5)>
                            word 27 : <value-histogram(5)>
                            word 28 : <value-histogram(5)>
                            word 29 : <value-histogram(5)>
                            word 30 : <value-histogram(5)>
                            word 31 :<saturation-histogram(0)>
                            word 32 :<saturation-histogram(1)>
                            word 33 :<saturation-histogram(2)>
                            word 34 :<saturation-histogram(3)>
                            word 35 :<saturation-histogram(4)>
                            """
                            object_line = file_handler.readline()
                            # print(object_line)
                            words = object_line.strip().split()
                            # print(words)
                            object_id = int(words[1])
                            object_name = words[0]
                            object_type_id = int(words[3])
                            object_type_name = words[2]
                            object_feature_list = Dataset.ObjectFeatures()
                            object_feature_list += words[4:]
                            # print(len(object_feature_list))
                            object = Dataset.Object(object_id,
                                                    object_name,
                                                    object_type_id,
                                                    object_type_name,
                                                    room_id,
                                                    object_feature_list)
                            room.objects.append(object)
                        # home.room_list.append(room)
                        """
                        Read the next line with the following structure:
                        word  0: N_relations
                        word  1: <number-of-relations>
                        word  2: N_relationFeatures
                        word  3: <number-of-features>
                        """
                        relations_header_line = file_handler.readline()
                        # print(relations_header_line)
                        words = relations_header_line.strip().split()
                        # print(words)
                        num_relations = int(words[1])
                        num_features_per_relation = int(words[3])
                        # Read the next num_relations lines
                        for object_relation_index in range(num_relations):
                            """
                            Read a line with the following structure:

                            word 0  : <label-obj-1>
                            word 1  : <label-obj-2>
                            word 2  : <relation-ID>
                            word 3  : <obj-1-ID>
                            word 4  : <obj-2-ID>
                            word 5  : <obj-1-ground-truth>
                            word 6  : <obj-2-ground-truth>
                            word 7  : <minimum-distance>
                            word 8  : <perpendicularity>
                            word 9  : <vertical-distance>
                            word 10 : <volume-ratio>
                            word 11 : <is-on>
                            word 12 : <abs-hue-stdv-diff>
                            word 13 : <abs-saturation-stdv-diff>
                            word 14 : <abs-value-stdv-diff>
                            word 15 : <abs-hue-mean-diff>
                            word 16 : <abs-saturation-mean-diff>
                            word 17 : <abs-value-mean-diff>
                            """
                            relation_line = file_handler.readline()
                            words = relation_line.strip().split()

                            object_relation_id = words[2]
                            object_relation_obj1_id   = words[3]
                            object_relation_obj1_name = words[0]
                            object_relation_obj1_type = words[5]
                            object_relation_obj2_id   = words[4]
                            object_relation_obj2_name = words[1]
                            object_relation_obj2_type = words[6]
                            object_relation_feature_list = Dataset.ObjectRelationFeatures()
                            object_relation_feature_list += words[7:]

                            object_relation = Dataset.ObjectRelation(
                                object_relation_id,
                                object_relation_obj1_id,
                                object_relation_obj1_name,
                                object_relation_obj1_type,
                                object_relation_obj2_id,
                                object_relation_obj2_name,
                                object_relation_obj2_type,
                                object_relation_feature_list
                            )
                            room.relations.append(object_relation)
                        """
                        Read the next line with the following structure:
                        word  0: N_observations
                        word  1: <number-of-observations>
                        word  2: N_roomFeatures
                        word  3: <number-of-room-features>
                        word  4: N_scanFeatures
                        word  5: <number-of-scan-features>
                        """
                        observations_header_line = file_handler.readline()
                        #print(observations_header_line)
                        words = observations_header_line.strip().split()
                        #print(words)
                        num_observations  = int(words[1])
                        num_room_features = int(words[3])
                        num_scan_features = int(words[5])
                        # Read the next num_relations lines
                        for observation_index in range(num_observations):
                            """
                            word  0 : <sensor-label>
                            word  1 : <observation-ID>
                            word  2 : <number-of-objects-in-obs>
                            word  3 : <object-ID> number-of-objects-in-obs times
                            jump number-of-objects-in-obs lines
                            word  4 (end - 55): <mean-hue>
                            word  5 (end - 54): <mean-saturation>
                            word  6 (end - 53): <mean-value> <hue-stdv>
                            word  7 (end - 52): <saturation-stdv>
                            word  8 (end - 51): <value-stdv>
                            word  9 (end - 46): <hue-histogram(5)>
                            word 14 (end - 41): <saturation-histogram(5)>
                            word 19 (end - 36): <value-histogram(5)>
                            word 24 (end - 35): <distance>
                            word 25 (end - 34): <foot-print>
                            word 26 (end - 33): <volume>
                            word 27 (end - 32): <mean-mean-hue>
                            word 28 (end - 31): <mean-mean-saturation>
                            word 29 (end - 30): <mean-mean-value>
                            word 30 (end - 29): <mean-hue-stdv>
                            word 31 (end - 28): <mean-saturation-stdv>
                            word 32 (end - 27): <mean-value-stdv>
                            word 33 (end - 22): <mean-hue-histogram(5)>
                            word 34 (end - 17): <mean-saturation-histogram(5)>
                            word 35 (end - 12): <mean-value-histogram(5)>
                            word 36 (end - 11): <mean-distance>
                            word 37 (end - 10): <mean-foot-print>
                            word 38 (end -  9): <mean-volume>
                            word 39 (end -  8): <area>
                            word 40 (end -  7): <elongation>
                            word 41 (end -  6): <mean-distance>
                            word 42 (end -  5): <distance-stdv>
                            word 43 (end -  4): <num-of-points>
                            word 44 (end -  3): <compactness>
                            word 45 (end -  2): <compactness2>
                            word 46 (end -  1): <linearity>
                            word 47 (end -  0): <scatter>
                            """
                            observations_line = file_handler.readline()
                            # print(observations_line)
                            words = observations_line.strip().split()
                            # print(observation_index, len(words))
                            # print(words)
                            observation_id = words[1]
                            observation_sensor_name = words[0]

                            """ compute range values """
                            obj_num = int(words[2])
                            obj_id_range_begin = 3
                            obj_id_range_end     = obj_id_range_begin + obj_num
                            obs_feat_range_begin = obj_id_range_end
                            obs_feat_range_end   = obs_feat_range_begin + 48
                            obs_scan_range_begin = obs_feat_range_end
                            obs_scan_range_end   = obs_scan_range_begin + 9
                            # print("[{},{}]".format(obj_id_range_begin,obj_id_range_end))
                            # print("[{},{}]".format(obs_feat_range_begin,obs_feat_range_end))
                            # print("[{},{}]".format(obs_scan_range_begin,obs_scan_range_end))

                            observation_objects_id = words[obj_id_range_begin:obj_id_range_end]

                            observation_features = Dataset.ObservationFeatures()
                            observation_features += words[obs_feat_range_begin:obs_feat_range_end]
                            # print(len(observation_features))

                            observation_scan_features = Dataset.ObservationScanFeatures()
                            observation_scan_features += words[obs_scan_range_begin:obs_scan_range_end]
                            # print(len(observation_scan_features))

                            observation = Dataset.Observation(
                                observation_id,
                                observation_sensor_name,
                                observation_objects_id,
                                observation_features,
                                observation_scan_features
                            )

                            room.observations.append(observation)
                        home.rooms.append(room)
                home_list.append(home)
            return home_list

            # print(self.home_files)

            """
            home_files_key = "alma-s1"
            home_file_name = "features_alma-s1_bathroom1.txt"
            path = self.path + "/" + home_files_key + "/" + home_file_name
            print(path)
            """


    def __init__(self, name=""):
        """
        Initializes the Dataset with supplied values

        Attributes
        =========

        name : Human name of
        unit : dict with the expected dataset units:
            http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html#downloads
        types : dict with homes, room categories and object categories
        """

        self.name = name
        self.unit = {}

        self.unit["raw"] = self.DatasetUnit(
          "Raw data",
          "https://ananas.isa.uma.es:10002/sharing/PAJxeUT0q",
          "Robot@Home-dataset_raw_data-plain_text-all",
          "4823b61180bbf8ce5458ad43ad709069edb0e8f3",
          20002442369)

        self.unit["lsrscan"] = self.DatasetUnit(
          "Laser scans",
          "https://ananas.isa.uma.es:10002/sharing/pMVKQb5hl",
          "Robot@Home-dataset_laser_scans-plain_text-all",
          "0f188931b2bce1926d0faaac13be78614749ec72",
          227829791)

        self.unit["rgbd"] = self.DatasetUnit(
          "RGB-D data",
          "https://ananas.isa.uma.es:10002/sharing/sJUC06jFJ",
          "Robot@Home-dataset_rgbd_data-plain_text-all",
          "b934e53d16580a62e0f4f1532d1efaa0567232ae",
          19896608308)

        self.unit["recscn"] = self.DatasetUnit(
          "Reconstructed scenes",
          "https://ananas.isa.uma.es:10002/sharing/sFCGRu1LN",
          "Robot@Home-dataset_reconstructed-scenes_plain-text_all",
          "5dc5aed9dfebf6e14890eb2418d3f518d0f55c6d",
          7947567151)

        self.unit["lblscn"] = self.DatasetUnit(
          "Labeled scenes",
          "https://ananas.isa.uma.es:10002/sharing/KS6kscXb3",
          "Robot@Home-dataset_labelled-scenes_plain-text_all",
          "394dc6c8f4d19b2887007e6ee66f2e7cb64f930f",
          7947369064)

        self.unit["lblrgbd"] = self.DatasetUnit(
          "Labeled RGB-D data",
          "https://ananas.isa.uma.es:10002/sharing/jVVI92AJn",
          "Robot@Home-dataset_labelled-rgbd-data_plain-text_all",
          "6834f930a16bb5d968d55b0b647703d952384e91",
          16739353847)

        self.unit["chelmnts"] = self.DatasetUnitCharacterizedElements(
            "Characterized elements",
            "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
            "Robot@Home-dataset_characterized-elements",
            "9d46bc3b33d2c6b84c04bd3db12cc415c17b4ae8",
            33345659
        )

        self.unit["2dgeomap"] = self.DatasetUnit(
          "2D geometric maps",
          "https://ananas.isa.uma.es:10002/sharing/PUZHG28p6",
          "Robot@Home-dataset_2d_geometric_maps",
          "a00bb33bc628e0fdb9df6822915b9eafcf67998f",
          8323899)

        self.unit["2dgeomapl"] = self.DatasetUnit(
          "2D geometric maps + logs",
          "https://ananas.isa.uma.es:10002/sharing/VLWRJUJGY",
          "Robot@Home-dataset_2d_geometric_maps+logs",
          "f8b3dadd9181291a59f589033521708d4399d12b",
          216384106)

        self.unit["hometopo"] = self.DatasetUnit(
          "Home's topologies",
          "https://ananas.isa.uma.es:10002/sharing/EBXypqYAV",
          "Robot@Home-dataset_homes-topologies",
          "652087d30c05ff4eaec9a0770307a2ced7fe5064",
          40872)

        # self.categories = self.unit["chelmnts"].load_categories()
        self.categories = self.unit["chelmnts"].categories

    def __str__(self):

        """ Units """
        total_expected_size = 0

        s = "\n" + self.name + "\n" + "*" * len(self.name) + "\n"*2
        s += "Units" + "\n" + "=====" + "\n"*2
        for unit in self.unit.values():
            s += unit.__str__()
            total_expected_size += unit.expected_size

        s += "\n"
        s += 'Total expected size = ' + str(total_expected_size) + \
             ' (' + humanize.naturalsize(total_expected_size) + ')'
        s += "\n"

        return s


def main():

    """
    Multiline comment
    """

    # http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html#downloads
    # /media/goyo/WDGREEN2TB-A/Users/goyo/Documents

    rhds = Dataset("MyRobot@Home")

    # print(rhds)

    """
    print(rhds["hometopo"].check_integrity(verbose=True))
    print(rhds["hometopo"].hash_for_directory())
    rhds["hometopo"].download()
    """
    # print(rhds.unit["chelmnts"])
    # home_dict = rhds.unit["chelmnts"].get_homes()
    # reversed_home_dict = dict(map(reversed, home_dict.items()))
    # print(home_dict)
    # print(reversed_home_dict)
    # print(rhds.unit["chelmnts"].get_rooms())
    # print(rhds.unit["chelmnts"].get_objects())

    """
    homes = rhds.unit["chelmnts"].homes
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

    print('######## HOME #########')
    home = rhds.unit["chelmnts"].homes[0]
    print(home)
    print(home.as_list())
    print(home.as_dict())

    print('######## HOMES #########')
    homes = rhds.unit["chelmnts"].homes
    print(homes)
    print(homes.get_ids())
    print(homes.get_names())
    print(homes.as_dict_id())
    print(homes.as_dict_name())

    print('######## HOME.ROOM #########')
    room = homes[0].rooms[0]
    print(room)
    print(room.as_list())
    print(room.as_dict())

    print('######## HOME.ROOMS #########')
    rooms = homes[0].rooms
    print(rooms)
    print(rooms.get_ids())
    print(rooms.get_names())
    print(rooms.as_dict_name())
    print(rooms.as_dict_id())

    print('######## HOME.ROOM.OBJECT #########')
    object = homes[0].rooms[0].objects[0]
    print(object)
    print(object.as_dict())

    print('######## HOME.ROOM.OBJECT.FEATURES #########')
    object_features = homes[0].rooms[0].objects[0].features
    print(object_features)
    print(object_features.as_dict())

    print('######## HOME.ROOM.OBJECTS #########')
    objects = homes[0].rooms[0].objects
    print(objects)
    print(objects.get_ids())
    print(objects.get_names())
    print(objects.as_dict_name())
    print(objects.as_dict_id())

    print('######## HOME.ROOM.RELATION #########')
    relation = homes[0].rooms[0].relations[0]
    print(relation)
    print(relation.as_list())
    print(relation.as_dict())

    print('######## HOMES.ROOMS.RELATION.FEATURES #########')
    relation_features = homes[0].rooms[0].relations[0].features
    print(relation_features)
    print(relation_features.as_dict())

    print('######## HOME.ROOM.RELATIONS #########')
    relations = homes[0].rooms[0].relations
    print(relations)
    print(relations.get_ids())
    print(relations.get_obj1_ids())
    print(relations.get_obj2_ids())
    print(relations.as_dict_id())
    #print(relations.as_dict_obj1_id())
    #print(relations.as_dict_obj2_id())

    print('######## HOME.ROOM.OBSERVATION #########')
    observation = homes[0].rooms[0].observations[0]
    print(observation)
    print(observation.as_list())
    print(observation.as_dict())

    print('######## HOME.ROOM.OBSERVATION.FEATURES #########')
    observation_features = homes[0].rooms[0].observations[0].features
    print(observation_features)
    print(observation_features.as_dict())

    print('######## HOME.ROOM.OBSERVATION.SCAN_FEATURES #########')
    observation_scan_features = homes[0].rooms[0].observations[0].scan_features
    print(observation_scan_features)
    print(observation_scan_features.as_dict())

    print('######## HOME.ROOM.OBSERVATIONS #########')
    observations = homes[0].rooms[0].observations
    print(observations)
    print(observations.get_ids())
    print(observations.get_sensor_names())
    print(observations.as_dict_id())
    #print(observations.as_dict_sensor_name())

    return 0


if __name__ == "__main__":
    main()
