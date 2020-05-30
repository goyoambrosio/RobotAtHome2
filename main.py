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

    def __init__(self, name="", url="", path="", hash_code=""):
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
        self.hash_code = hash_code

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


    rhds = []
    rhds.append(Dataset("Raw data",
                        "https://ananas.isa.uma.es:10002/sharing/PAJxeUT0q",
                        "Robot@Home-dataset_raw_data-plain_text-all",
                        "4823b61180bbf8ce5458ad43ad709069edb0e8f3"))

    rhds.append(Dataset("Laser scans",
                        "https://ananas.isa.uma.es:10002/sharing/pMVKQb5hl",
                        "Robot@Home-dataset_laser_scans-plain_text-all",
                        "0f188931b2bce1926d0faaac13be78614749ec72"))

    rhds.append(Dataset("RGB-D data",
                        "https://ananas.isa.uma.es:10002/sharing/sJUC06jFJ",
                        "Robot@Home-dataset_rgbd_data-plain_text-all",
                        "b934e53d16580a62e0f4f1532d1efaa0567232ae"))

    rhds.append(Dataset("Reconstructed scenes",
                        "https://ananas.isa.uma.es:10002/sharing/sFCGRu1LN",
                        "Robot@Home-dataset_reconstructed-scenes_plain-text_all",
                        "5dc5aed9dfebf6e14890eb2418d3f518d0f55c6d"))

    rhds.append(Dataset("Labeled scenes",
                        "https://ananas.isa.uma.es:10002/sharing/KS6kscXb3",
                        "Robot@Home-dataset_labelled-scenes_plain-text_all",
                        "394dc6c8f4d19b2887007e6ee66f2e7cb64f930f"))

    rhds.append(Dataset("Labeled RGB-D data",
                        "https://ananas.isa.uma.es:10002/sharing/jVVI92AJn",
                        "Robot@Home-dataset_labelled-rgbd-data_plain-text_all",
                        "6834f930a16bb5d968d55b0b647703d952384e91"))

    rhds.append(Dataset("Characterized elements",
                        "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
                        "Robot@Home-dataset_characterized-elements",
                        "9d46bc3b33d2c6b84c04bd3db12cc415c17b4ae8"))

    rhds.append(Dataset("2D geometric maps",
                        "https://ananas.isa.uma.es:10002/sharing/PUZHG28p6",
                        "Robot@Home-dataset_2d_geometric_maps",
                        "a00bb33bc628e0fdb9df6822915b9eafcf67998f"))

    rhds.append(Dataset("2D geometric maps + logs",
                        "https://ananas.isa.uma.es:10002/sharing/VLWRJUJGY",
                        "Robot@Home-dataset_2d_geometric_maps+logs",
                        "f8b3dadd9181291a59f589033521708d4399d12b"))

    rhds.append(Dataset("Home's topologies",
                        "https://ananas.isa.uma.es:10002/sharing/EBXypqYAV",
                        "Robot@Home-dataset_homes-topologies",
                        "652087d30c05ff4eaec9a0770307a2ced7fe5064"))

    # h = fire.Fire(hash_for_directory)

    rhds = {}

    rhds["raw"] = Dataset(
      "Raw data",
      "https://ananas.isa.uma.es:10002/sharing/PAJxeUT0q",
      "Robot@Home-dataset_raw_data-plain_text-all",
      "4823b61180bbf8ce5458ad43ad709069edb0e8f3")

    rhds["lsrscan"] = Dataset(
      "Laser scans",
      "https://ananas.isa.uma.es:10002/sharing/pMVKQb5hl",
      "Robot@Home-dataset_laser_scans-plain_text-all",
      "0f188931b2bce1926d0faaac13be78614749ec72")

    rhds["rgbd"] = Dataset(
      "RGB-D data",
      "https://ananas.isa.uma.es:10002/sharing/sJUC06jFJ",
      "Robot@Home-dataset_rgbd_data-plain_text-all",
      "b934e53d16580a62e0f4f1532d1efaa0567232ae")

    rhds["recscn"] = Dataset(
      "Reconstructed scenes",
      "https://ananas.isa.uma.es:10002/sharing/sFCGRu1LN",
      "Robot@Home-dataset_reconstructed-scenes_plain-text_all",
      "5dc5aed9dfebf6e14890eb2418d3f518d0f55c6d")

    rhds["lblscn"] = Dataset(
      "Labeled scenes",
      "https://ananas.isa.uma.es:10002/sharing/KS6kscXb3",
      "Robot@Home-dataset_labelled-scenes_plain-text_all",
      "394dc6c8f4d19b2887007e6ee66f2e7cb64f930f")

    rhds["lblrgbd"] = Dataset(
      "Labeled RGB-D data",
      "https://ananas.isa.uma.es:10002/sharing/jVVI92AJn",
      "Robot@Home-dataset_labelled-rgbd-data_plain-text_all",
      "6834f930a16bb5d968d55b0b647703d952384e91")

    rhds["chelmnt"] = Dataset(
      "Characterized elements",
      "https://ananas.isa.uma.es:10002/sharing/t6zVblP3w",
      "Robot@Home-dataset_characterized-elements",
      "9d46bc3b33d2c6b84c04bd3db12cc415c17b4ae8")

    rhds["2dgeomap"] = Dataset(
      "2D geometric maps",
      "https://ananas.isa.uma.es:10002/sharing/PUZHG28p6",
      "Robot@Home-dataset_2d_geometric_maps",
      "a00bb33bc628e0fdb9df6822915b9eafcf67998f")

    rhds["2dgeomapl"] = Dataset(
      "2D geometric maps + logs",
      "https://ananas.isa.uma.es:10002/sharing/VLWRJUJGY",
      "Robot@Home-dataset_2d_geometric_maps+logs",
      "f8b3dadd9181291a59f589033521708d4399d12b")

    rhds["hometopo"] = Dataset(
      "Home's topologies",
      "https://ananas.isa.uma.es:10002/sharing/EBXypqYAV",
      "Robot@Home-dataset_homes-topologies",
      "652087d30c05ff4eaec9a0770307a2ced7fe5064")


    print (len(rhds))
    for x in rhds:
      print(x)
      print(rhds[x].name)

# https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
# https://pypi.org/project/humanize/

    return 0

if __name__ == "__main__":
    main()
