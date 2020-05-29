#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is the docstring"""

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/05/29"
__license__ = "GPLv3"

import fire
import os.path
from os import path
import os
import hashlib


class Dataset(object):

    """
    A plain text Robot@Home dataset
    """
    roar = "I'm a dataset"

    def __init__(self, name='', url='', path=''):
        """
        Initializes the dataset with supplied values

        Attributes
        =========

        name : Human name of
        url  : url string to download it
        path : root path of
        """
        self.name = name
        self.url = url
        self.path = path

def hash_for_directory(path, hashfunc=hashlib.sha1):
    """
    Computes a single hash for a given folder. It works fine for small-sized
    files (e.g. a source tree or something, where every file individually can
    fit into RAM easily), ignoring empty directories.

    It works like this:

    1. Find all files in the directory recursively and sort them by name
    2. Calculate the hash (default: SHA-1) of every file (reads whole file into memory)
    3. Make a textual index with "filename=hash" lines
    4. Encode that index back into a UTF-8 byte string and hash that

    You can pass in a different hash function
    (https://docs.python.org/3/library/hashlib.html) as second parameter

    Source:
    https://stackoverflow.com/questions/545387/linux-compute-a-single-hash-for-a-given-folder-contents

    Other options:
    https://stackoverflow.com/questions/24937495/how-can-i-calculate-a-hash-for-a-filesystem-directory-using-python
    """
    filenames = sorted(os.path.join(dp, fn) for dp, _, fns in os.walk(path) for fn in fns)
    index = '\n'.join('{}={}'.format(os.path.relpath(fn, path), hashfunc(open(fn, 'rb').read()).hexdigest()) for fn in filenames)
    return hashfunc(index.encode('utf-8')).hexdigest()

def main():

    """
    Multiline comment
    """

    # http://mapir.isa.uma.es/mapirwebsite/index.php/mapir-downloads/203-robot-at-home-dataset.html#downloads
    # /media/goyo/WDGREEN2TB-A/Users/goyo/Documents

    sessions = ("alma-s1",
                "anto-s1",
                "pare-s1",
                "rx2-s1",
                "sarmis-s1",
                "sarmis-s2",
                "sarmis-s3")

    data = ("Raw data",
            "Laser scans",
            "RGB-D data",
            "Reconstructed scenes",
            "Labeled scenes",
            "Labeled RGB-D data",
            "Characterized elements",
            "2D geometric maps",
            "2D geometric maps + logs",
            "Home's topologies")

    urls = ("https://ananas.isa.uma.es:10002/sharing/PAJxeUT0q",
            "https://ananas.isa.uma.es:10002/sharing/pMVKQb5hl",
            "https://ananas.isa.uma.es:10002/sharing/sJUC06jFJ",
            "https://ananas.isa.uma.es:10002/sharing/sFCGRu1LN",
            "https://ananas.isa.uma.es:10002/sharing/KS6kscXb3",
            "https://ananas.isa.uma.es:10002/sharing/jVVI92AJn",
            "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
            "https://ananas.isa.uma.es:10002/sharing/PUZHG28p6",
            "https://ananas.isa.uma.es:10002/sharing/VLWRJUJGY",
            "https://ananas.isa.uma.es:10002/sharing/EBXypqYAV")

    paths = ("Robot@Home-dataset_raw_data-plain_text-all",
             "Robot@Home-dataset_laser_scans-plain_text-all",
             "Robot@Home-dataset_rgbd_data-plain_text-all",
             "Robot@Home-dataset_reconstructed-scenes_plain-text_all",
             "Robot@Home-dataset_labelled-scenes_plain-text_all",
             "Robot@Home-dataset_labelled-rgbd-data_plain-text_all",
             "Robot@Home-dataset_characterized-elements",
             "Robot@Home-dataset_2d_geometric_maps",
             "Robot@Home-dataset_2d_geometric_maps+logs",
             "Robot@Home-dataset_homes-topologies")

    rhds = []
    rhds.append(Dataset("Raw data",
                        "https://ananas.isa.uma.es:10002/sharing/PAJxeUT0q",
                        "Robot@Home-dataset_raw_data-plain_text-all"))
    rhds.append(Dataset("Laser scans",
                        "https://ananas.isa.uma.es:10002/sharing/pMVKQb5hl",
                        "Robot@Home-dataset_laser_scans-plain_text-all"))
    rhds.append(Dataset("RGB-D data",
                        "https://ananas.isa.uma.es:10002/sharing/sJUC06jFJ",
                        "Robot@Home-dataset_rgbd_data-plain_text-all"))
    rhds.append(Dataset("Reconstructed scenes",
                        "https://ananas.isa.uma.es:10002/sharing/sFCGRu1LN",
                        "Robot@Home-dataset_reconstructed-scenes_plain-text_all"))
    rhds.append(Dataset("Labeled scenes",
                        "https://ananas.isa.uma.es:10002/sharing/KS6kscXb3",
                        "Robot@Home-dataset_labelled-scenes_plain-text_all"))
    rhds.append(Dataset("Labeled RGB-D data",
                        "https://ananas.isa.uma.es:10002/sharing/jVVI92AJn",
                        "Robot@Home-dataset_labelled-rgbd-data_plain-text_all"))
    rhds.append(Dataset("Characterized elements",
                        "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
                        "Robot@Home-dataset_characterized-elements"))
    rhds.append(Dataset("2D geometric maps",
                        "https://ananas.isa.uma.es:10002/sharing/PUZHG28p6",
                        "Robot@Home-dataset_2d_geometric_maps"))
    rhds.append(Dataset("2D geometric maps + logs",
                        "https://ananas.isa.uma.es:10002/sharing/VLWRJUJGY",
                        "Robot@Home-dataset_2d_geometric_maps+logs"))
    rhds.append(Dataset("Home's topologies",
                        "https://ananas.isa.uma.es:10002/sharing/EBXypqYAV",
                        "Robot@Home-dataset_homes-topologies"))

    h = fire.Fire(hash_for_directory)
    

    return 0

if __name__ == "__main__":
    main()
