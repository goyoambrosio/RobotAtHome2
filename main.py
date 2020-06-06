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
    class home():
        def __init__(self, id, name, room_list=[]):
            self.id = id
            self.name = name
            self.room_list = room_list

    class room():
        def __init__(self, id, type_id, home_id, object_list=[]):
            self.id = id
            self.type_id = type_id
            self.home_id = home_id
            self.objects_list = object_list

    class object():
        def __init__(self, id, name, type_id, room_id, feature_list=[]):
            self.id = id
            self.name = name
            self.room_id = room_id
            self.feature_list = feature_list

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

        def load_home_file(self):
            """
            """
            home_list = []
            room_list = []

            home_dict = self.get_homes()
            reversed_home_dict = dict(map(reversed, home_dict.items()))

            for home_files_key, home_files_value in self.home_files.items():
                home_name = home_files_key
                home_id = int(reversed_home_dict[home_files_key])
                home = Dataset.home(home_id, home_name)
                for home_file_name in home_files_value:
                    path = self.path + "/" + home_files_key + "/" + \
                           home_file_name
                    print(path)
                    with open(path, "r") as file_handler:
                        # Read the first line
                        home_header = file_handler.readline()
                        words = home_header.strip().split()
                        print(words)
                        room_id         = words[7]
                        room_type_id    = words[6]
                        num_of_objects  = int(words[9])
                        num_of_features  = int(words[11])
                        room = Dataset.room(room_id, room_type_id, home_id)

                        for object_index in range(1, num_of_objects):
                            object_line = file_handler.readline()
                            words = object_line.strip().split()
                            print(words)
                            object_name = words[0]
                            object_id = words[1]
                            object_type_id = words[3]
                            object_feature_list = words[4:num_of_features + 3]
                            object = Dataset.object(object_id, object_name,
                                                    object_type_id, room_id,
                                                    object_feature_list)

                            # for feature_index in range(1, num_of_features):
                            #    object_feature_list.append(words[feature_index+3])
                            room.objects_list.append(object)
                        home.room_list.append(room)
                home_list.append(home)

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
    home_dict = rhds.unit["chelmnts"].get_homes()
    reversed_home_dict = dict(map(reversed, home_dict.items()))
    print(home_dict)
    print(reversed_home_dict)
    # print(rhds.unit["chelmnts"].get_rooms())
    # print(rhds.unit["chelmnts"].get_objects())

    rhds.unit["chelmnts"].load_home_file()

    return 0


if __name__ == "__main__":
    main()
