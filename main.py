#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is the docstring"""

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/05/29"
__license__ = "GPLv3"

import fire
import os
import hashlib
import humanize
import requests
import wget
import ssl
import re


class Dataset():

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
            s = self.name + '\n' + \
                '  url           = ' + self.url + '\n' + \
                '  path          = ' + self.path + '\n' + \
                '  expected hash = ' + self.expected_hash_code + '\n' + \
                '  expected size = ' + str(self.expected_size) + ' bytes  (' + \
                humanize.naturalsize(self.expected_size) + ')' + '\n'
            return s

        def check_folder_size(self, verbose=False):
            """
            Check that the expected size match with the real folder size
            verbose  : it outputs additional printed details
            """
            real_folder_size = self.size(self.path)
            if verbose:
                print('expected size : ' + str(self.expected_size) + ' bytes (' +
                      humanize.naturalsize(self.expected_size) + ')')
                print('counted       : ' + str(real_folder_size) + ' bytes (' +
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
                    return sum(self.size(entry, follow_symlinks=follow_symlinks)
                               for entry in it)
            except NotADirectoryError:
                return os.stat(path, follow_symlinks=follow_symlinks).st_size

        def hash_for_directory(self, hashfunc=hashlib.sha1):
            """
            Computes a single hash for a given folder. It works fine for
            small-sized files (e.g. a source tree or something, where every file
            individually can fit into RAM easily), ignoring empty directories.

            It works like this:

            1. Find all files in the directory recursively and sort them by name
            2. Calculate the hash (default: SHA-1) of every file (reads whole file
               into memory)
            3. Make a textual index with "filename=hash" lines
            4. Encode that index back into a UTF-8 byte string and hash that

            You can pass in a different hash function
            (https://docs.python.org/3/library/hashlib.html) as second parameter

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

    class DatasetUnitCharacterizedElemets(DatasetUnit):
        def get_sessions(self):
            sessions = {"alma-s1",
                        "anto-s1",
                        "pare-s1",
                        "rx2-s1",
                        "sarmis-s1",
                        "sarmis-s2",
                        "sarmis-s3"}
            return sessions

        def get_types(self):
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

    def __init__(self, name=""):
        """
        Initializes the Dataset with supplied values

        Attributes
        =========

        name : Human name of
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

        self.unit["chelmnts"] = self.DatasetUnitCharacterizedElemets(
          "Characterized elements",
          "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
          "Robot@Home-dataset_characterized-elements",
          "9d46bc3b33d2c6b84c04bd3db12cc415c17b4ae8",
          33345659)

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


def main():

    """
    Multiline comment
    """

    # http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html#downloads
    # /media/goyo/WDGREEN2TB-A/Users/goyo/Documents

    rhds = Dataset("MyRobot@Home")
    """
    print('Robot@Home dataset units: ' + str(len(rhds.unit)))
    print('============================')
    total_expected_size = 0
    for x in rhds.unit:
        total_expected_size = total_expected_size + rhds.unit[x].expected_size
        print('(' + x + ')')
        print(rhds.unit[x])
        # print('  Check size: ' + str(rhds.unit[x].check_folder_size()))
    print('Total expected size = ' + str(total_expected_size) + ' (' +
          humanize.naturalsize(total_expected_size) + ')')
    """
    """
    print(rhds["hometopo"].check_integrity(verbose=True))
    print(rhds["hometopo"].hash_for_directory())
    rhds["hometopo"].download()
    """
    print(rhds.unit["chelmnts"].get_types())

    return 0


if __name__ == "__main__":
    main()
