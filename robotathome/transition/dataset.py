#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home Python API """

__author__ = "Gregorio Ambrosio Cestero"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, 2021, Gregorio Ambrosio Cestero"
__date__ = "2021/02/03"
__license__ = "MIT"

import version
import os
import hashlib
import humanize
import cv2
import numpy as np
import sys
import time
import tarfile
import click
from urllib.request import urlretrieve
from urllib.request import urlopen
import cgi
import io
#import progressbar
# from memory_profiler import profile

class Dataset():

    class DatasetUnit():

        """
        A plain text Robot@Home dataset
        """

        def __init__(self,
                     name = "",
                     path = "",
                     url = "",
                     expected_hash_code="",
                     expected_size = 0):
            """
            Initializes the DatasetUnit with supplied values

            Attributes
            =========

            name : Human name of
            path : root path of
            url  : url string to download it
            expected_hash_code : the hash code the downloaded unit must have
            expected_size      : the number of bytes the downloaded copy must
                                 have
            """

            self.name = name
            self.path = path
            self.url = url
            self.expected_hash_code = expected_hash_code
            self.expected_size = expected_size
            self.__data_loaded__ = False

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
            print("Computing use disk space for folder: \n%s \nIt may take some time for huge data units" % self.path)
            real_folder_size = self.size(self.path)
            if verbose:
                print('expected size : ' + str(self.expected_size) +
                      ' bytes (' +
                      humanize.naturalsize(self.expected_size) + ')')
                print('computed size : ' + str(real_folder_size) +
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
                print('Unit          : ' + self.name)
                print('Folder path   : ' + self.path)
            folder_exist = os.path.isdir(self.path)
            if verbose:
                print('Folder exist  : ' + str(folder_exist))
            if folder_exist:
                correct_size = self.check_folder_size(verbose)
                if verbose:
                    print('Correct size  : ' + str(correct_size))
            return folder_exist and correct_size

        def download(self):

            downloaded = False

            # urlretrieve progression stuff
            def reporthook(count, block_size, total_size):
                global start_time
                if count == 0:
                    start_time = time.time()
                    return
                duration = time.time() - start_time
                progress_size = int(count * block_size)
                speed = int(progress_size * 8 / 1024 / (1024 * duration))
                percent = min(int(count * block_size * 100 / total_size), 100)
                expected_duration = (total_size / 1048576 * 8) / speed - duration
                sys.stdout.write("\rProgress: %d%%, %d MB / %d MB, %d Mb/s, %d seconds , %d seconds left" % (percent, progress_size / 1048576, total_size / 1048576, speed, duration, expected_duration))
                sys.stdout.flush()

            # bar = None
            # def reporthook1(block_num, block_size, total_size):
            #     pbar = bar
            #     if pbar is None:
            #          widgets = ['Progress: ',
            #                     progressbar.Percentage(),  ' ',
            #                     progressbar.Bar(marker='#', left='[', right=']'), ' ',
            #                     progressbar.ETA(), ' ',
            #                     progressbar.FileTransferSpeed()]
            #          pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_size).start()
            #     pbar.update(min(block_num * block_size, total_size))


            # print(filename)

            # tar progression stuff
            def get_file_progress_file_object_class(on_progress):
                   class FileProgressFileObject(tarfile.ExFileObject):
                       def read(self, size, *args):
                         on_progress(self.name, self.position, self.size)
                         return tarfile.ExFileObject.read(self, size, *args)
                   return FileProgressFileObject

            class TestFileProgressFileObject(tarfile.ExFileObject):
                   def read(self, size, *args):
                     on_progress(self.name, self.position, self.size)
                     return tarfile.ExFileObject.read(self, size, *args)

            class ProgressFileObject(io.FileIO):
                   def __init__(self, path, *args, **kwargs):
                       self._total_size = os.path.getsize(path)
                       io.FileIO.__init__(self, path, *args, **kwargs)

                   def read(self, size):
                       sys.stdout.write("\rProcessing %d of %d MB (%d%%)" % (self.tell() / 1048576, self._total_size / 1048576, self.tell()*100/self._total_size))
                       sys.stdout.flush()
                       return io.FileIO.read(self, size)

            def on_progress(filename, position, total_size):
                   print("%s: %d of %s" %(filename, position, total_size))

            # Main process

            # Get filename from remote
            remotefile = urlopen(self.url)
            blah = remotefile.info()['Content-Disposition']
            value, params = cgi.parse_header(blah)
            remote_filename = params["filename"]
            local_filename = os.path.dirname(self.path) + "/" + remote_filename
            #breakpoint()
            # main loop
            while downloaded is not True:
                if os.path.exists(local_filename) is False:
                    print("Downloading ", local_filename)
                    urlretrieve(self.url, local_filename, reporthook)
                    print("\n")
                else:
                    print ("It seems the file ", remote_filename, " already exists")

                if self.expected_hash_code != "":
                    print("Computing MD5 checksum")
                    checksum = self.get_md5_from_file(local_filename)
                    if checksum != self.expected_hash_code:
                        print('The MD5 checksum of local file %s differs from the remote %s.' %
                              (os.path.basename(local_filename), self.expected_hash_code))
                        if click.confirm('Do you want to remove ' + os.path.basename(local_filename) + ' ?', default=True):
                            os.remove(local_filename)
                        else:
                            return downloaded
                    else:
                        print("The local file MD5 checksum match the remote one")
                        # Extraction stuff
                        try:
                            print("Extracting files from %s: " % (os.path.basename(local_filename)))
                            tarfile.TarFile.fileobject = get_file_progress_file_object_class(on_progress)
                            tf = tarfile.open(fileobj=ProgressFileObject(local_filename))
                            tf.extractall(path=os.path.dirname(self.path))
                        except:
                            print("Something went wrong with the extraction process. Data could be corrupted")
                        else:
                            tf.close()
                            print()
                            print("Extraction success. Don't forget to remove %s if you are not plenty of space." % (os.path.basename(local_filename)))
                            downloaded = True
                            # print ("Removing ", os.path.basename(local_filename))
                            # os.remove(local_filename)
            return downloaded

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

        def get_md5_from_file(self, filename):
            BLOCKSIZE = 65536
            hasher = hashlib.md5()
            with open(filename, 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            print("MD5 checksum for %s : %s" % (os.path.basename(filename), hasher.hexdigest()))
            return hasher.hexdigest()

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

        def is_loaded(self):
            return self.__data_loaded__

        def load_data(self):

            title = "Dataset Unit: " + self.name
            print()
            print(title)
            print("=" * len(title))
            while True:
                try:
                    print("Trying to load data from: " + self.path)
                    self._load_function()  # this function must be defined in child class
                    print("Success ! Now data is loaded in memory. Use the API to access data")
                    self.__data_loaded__ = True
                    return self.__data_loaded__
                except:
                    print("Something went wrong: ",sys.exc_info()[0], " occurred.")
                    print("Checking the integrity. It can take some time, please be patient")
                    if (self.check_integrity(verbose=True)):
                        print("Seems to have passed the integrity check but some unknown error persists.")
                        print("It must be due to some external factor unrelated to this software.")
                    if click.confirm('Do you want to download ' + os.path.basename(self.path) + ' ?', default=True):
                        self.download()
                    else:
                        print("Data was not loaded. Trying to access data through API will raise errors")
                        self.__data_loaded__ = False
                        return self.__data_loaded__

        def get_type(self):
            return str(type(self)).split('.')[-1][:-2]

    class DatasetUnitCharacterizedElements(DatasetUnit):
        class HomeSession():
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
                s = "<HomeSession instance (" + str(self.id) + ":" + self.name + ")>"
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

            def get_home_name(self):
                return self.name.split('-s')[0]

        class HomeSessions(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<HomeSessions list instance (" + str(len(self)) + " items)>"
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
            12 : <saturation-mean>
            13 : <value-mean>
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
                    'saturation-mean',
                    'value-mean',
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
                    "\t" + "value-mean            : " + self[13] + "\n" + \
                    "\t" + "hue-stdv             : " + self[14] + "\n" + \
                    "\t" + "saturation-stdv      : " + self[15] + "\n" + \
                    "\t" + "value-std           : " + self[16] + "\n" + \
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

        def __init__(self, name="",
                     path="",
                     url="",
                     expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, path, url, expected_hash_code,
                             expected_size)
            self.__categories_file = "types.txt"
            self.__home_key_string = "home"
            self.__room_key_string = "room"
            self.__object_key_string = "object"

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

        def _load_function(self):
            self.categories = self.__load_categories()
            self.home_files = self.__get_home_files()
            self.home_sessions = self.__load_home_files()

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

        def get_category_home_sessions(self):
            for key in self.categories.keys():
                if self.__home_key_string in key.lower():
                    return self.categories[key]

        def get_home_names(self):
            category_homes = []
            for key in self.get_category_home_sessions().values():
                splitted_key = key.split('-s')
                if splitted_key[0] not in category_homes:
                    category_homes.append(str(splitted_key[0]))
            return category_homes

        def get_category_rooms(self):
            for key in self.categories.keys():
                if self.__room_key_string in key.lower():
                    return self.categories[key]

        def get_category_objects(self):
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
            home_list = list(self.get_category_home_sessions().values())
            for home in home_list:
                home_file[home] = os.listdir(self.path + '/' + home)
            return home_file

        def __load_home_files(self):
            """
            """
            home_sessions_list = self.HomeSessions()
            home_sessions_dict = self.get_category_home_sessions()
            reversed_home_sessions_dict = dict(map(reversed, home_sessions_dict.items()))

            for home_files_key, home_files_value in self.home_files.items():
                home_name = home_files_key
                home_id = int(reversed_home_sessions_dict[home_files_key])
                room_list = self.Rooms()
                home_session = self.HomeSession(home_id, home_name, room_list)
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
                        room_name       = home_file_name.split('.')[0][len('features_')+len(home_name)+1:]
                        room_type_id    = int(words[5])
                        room_type_name  = words[4]
                        num_of_objects  = int(words[9])
                        num_of_features = int(words[11])
                        objects         = self.Objects()
                        relations       = self.ObjectRelations()
                        observations    = self.Observations()
                        room = self.Room(room_id, room_name,
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
                            object_feature_list = self.ObjectFeatures()
                            object_feature_list += words[4:]
                            # print(len(object_feature_list))
                            object = self.Object(object_id,
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
                            object_relation_feature_list = self.ObjectRelationFeatures()
                            object_relation_feature_list += words[7:]

                            object_relation = self.ObjectRelation(
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

                            observation_features = self.ObservationFeatures()
                            observation_features += words[obs_feat_range_begin:obs_feat_range_end]
                            # print(len(observation_features))

                            observation_scan_features = self.ObservationScanFeatures()
                            observation_scan_features += words[obs_scan_range_begin:obs_scan_range_end]
                            # print(len(observation_scan_features))

                            observation = self.Observation(
                                observation_id,
                                observation_sensor_name,
                                observation_objects_id,
                                observation_features,
                                observation_scan_features
                            )

                            room.observations.append(observation)
                        home_session.rooms.append(room)
                home_sessions_list.append(home_session)
            return home_sessions_list

    class DatasetUnit2DGeometricMaps(DatasetUnit):
        class Home():
            def __init__(self, name, rooms):
                self.name = name
                self.rooms = rooms

            def __str__(self):
                s = '\t' + self.name
                return s

            def __repr__(self):
                s = "<Home instance (" + self.name + ")>"
                return s

        class Homes(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Homes list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [home.name for home in self]

        class Room():
            def __init__(self, name, points):
                self.name = name
                self.points = points

            def __str__(self):
                s = '\t' + self.name
                return s

            def __repr__(self):
                s = "<Room instance (" + self.name + ")>"
                return s

        class Rooms(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Rooms list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class Point():
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

            def __str__(self):
                s = '\t' + '(' + self.x + ',' + self.y + ',' + self.z + ')'
                return s

            def __repr__(self):
                s = "<Point instance>"
                return s

            def get_list(self):
                return [self.x, self.y, self.z]

        class Points(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Points list instance (" + str(len(self)) + \
                    " items)>"
                return s


        def __init__(self, name="",
                     url="",
                     path="",
                     expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)

        def _load_function(self):

            self.homes = self.Homes()
            # print(self.path + '/' + os.path.basename(self.path))
            home_folders_path = self.path + '/' + os.path.basename(self.path)
            home_folders = os.listdir(home_folders_path)
            # print(home_folders)
            for home_folder in home_folders:
                # print(home_folder)
                rooms = self.Rooms()
                room_files_path = home_folders_path + '/' + home_folder
                # print(room_files_path)
                room_files = os.listdir(room_files_path)
                # print(room_files)
                for room_file in room_files:
                    # print(room_file)
                    room_file_splitted = room_file.split('_')
                    room_file_path = room_files_path + '/' + room_file
                    points = self.Points()
                    with open(room_file_path, "r") as file_handler:
                        for line in file_handler:
                            words = line.strip().split()
                            # print(line)
                            # print(words)
                            point = self.Point(words[0], words[1], words[2])
                            points.append(point)
                            # print(point)

                    room = self.Room(room_file_splitted[0], points)
                    rooms.append(room)
                # print(rooms)
                home = self.Home(home_folder, rooms)
                self.homes.append(home)

        def __str__(self):
            tab = 4
            s = ""
            # s = str(self.homes).expandtabs(0) + "\n"
            for home in self.homes:
                s += str(home).expandtabs(0) + "\n"
                # print(str(home.rooms).expandtabs(tab*1))
                for room in home.rooms:
                    s += str(room).expandtabs(tab*1) + "\n"
                    s += '        number of points: ' + str(len(room.points)) + "\n"
            return super().__str__() + s

    class DatasetUnitHomesTopologies(DatasetUnit):
        class Home():
            def __init__(self, name, topo_relations):
                self.name = name
                self.topo_relations = topo_relations

            def __str__(self):
                s = '\t' + self.name + ' (' + str(len(self.topo_relations)) + \
                    ') topology relations' 
                return s

            def __repr__(self):
                s = "<Home instance (" + self.name + ")>"
                return s

            def as_dict(self):
                return {self.name: self.topo_relations}

        class Homes(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Homes list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def as_dict(self):
                keys = [home.name for home in self]
                values = [home.topo_relations for home in self]
                zip_obj = zip(keys, values)
                new_dict = dict(zip_obj)
                return new_dict


            def get_names(self):
                return [home.name for home in self]

        class TopoRelation():
            def __init__(self, room1_name, room2_name):
                self.room1_name = room1_name
                self.room2_name = room2_name

            def __str__(self):
                s = '\t' + self.room1_name + ' - ' + self.room2_name
                return s

            def __repr__(self):
                s = "<TopoRelation instance (" + self.name + ")>"
                return s

            def as_list(self):
                return [self.room1_name,self.room2_name]

            def as_dict(self):
                return {self.room1_name: self.room2_name}

        class TopoRelations(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<TopoRelations list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def as_dict(self):
                new_dict = {}
                for topo_relation in self:
                    new_dict[topo_relation.room1_name] = \
                            topo_relation.room2_name
                return new_dict

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)

            # self.homes = self.__load_data()

        def _load_function(self):
            self.homes = self.Homes()
            home_files = os.listdir(self.path)
            for home_file in home_files:
                if home_file.endswith('.txt'):
                    path = self.path + '/' + home_file
                    home_name = home_file.split('.')[0]
                    topo_relations = self.TopoRelations()
                    with open(path, "r") as file_handler:
                        for line in file_handler:
                            words = line.strip().split('-')
                            topo_relation = self.TopoRelation(words[0],
                                                              words[1])
                            topo_relations.append(topo_relation)
                    home = self.Home(home_name, topo_relations)
                    self.homes.append(home)
            # return homes

        def __str__(self):
            tab = 4
            s = ""
            # s = str(self.homes).expandtabs(0) + "\n"
            for home in self.homes:
                s += str(home).expandtabs(0) + "\n"
                for home in self.homes:
                    s += str(home.topo_relations).expandtabs(1) + "\n"
                    for topo_relation in home.topo_relations:
                        s += str(topo_relation).expandtabs(tab*2) + "\n"
            return super().__str__() + s

    class DatasetUnitRawData(DatasetUnit):

        class HomeSession():
            def __init__(self, name, rooms):
                self.name = name
                self.rooms = rooms

            def __str__(self):
                s = '\t' + self.name
                return s

            def __repr__(self):
                s = "<HomeSession instance (" + self.name + ")>"
                return s

            def get_home_name(self):
                return self.name.split('-s')[0]

        class HomeSessions(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<HomesSessions list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [home.name for home in self]

        class Room():
            def __init__(self, name, folder_path, sensor_observations):
                self.name = name
                self.folder_path = folder_path
                self.sensor_observations = sensor_observations

            def __str__(self):
                s = '\t' + self.name + '  folder: /' + self.folder_path + \
                    ' # observations: ' + str(len(self.sensor_observations))
                return s

            def __repr__(self):
                s = "<Room instance (" + self.name + ")>"
                return s

        class Rooms(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Rooms list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class Sensor():
            def __init__(self, id='0', name='undefined',
                         sensor_pose_x='0', sensor_pose_y='0', sensor_pose_z='0',
                         sensor_pose_yaw='0', sensor_pose_pitch='0', sensor_pose_roll='0',
                         time_stamp='0', files=[], path="", rel_path=""):
                self.id = id
                self.name = name
                self.sensor_pose_x = sensor_pose_x
                self.sensor_pose_y = sensor_pose_y
                self.sensor_pose_z = sensor_pose_z
                self.sensor_pose_yaw = sensor_pose_yaw
                self.sensor_pose_pitch = sensor_pose_pitch
                self.sensor_pose_roll = sensor_pose_roll
                self.time_stamp = time_stamp
                self.files = files
                self.path = path
                self.rel_path = rel_path

            def __str__(self):
                s = '\t' + self.id + ', ' + self.name + ', ' + \
                    self.sensor_pose_x + ', ' + \
                    self.sensor_pose_y + ', ' + \
                    self.sensor_pose_z + ', ' + \
                    self.sensor_pose_yaw + ', ' + \
                    self.sensor_pose_pitch + ', ' + \
                    self.sensor_pose_roll + ', ' + \
                    self.time_stamp + ', ' + \
                    str(self.files)
                return s

            def __repr__(self):
                s = "<Sensor instance (" + self.name + ")>"
                return s

            def load_files(self):

                """
                The path should be the room.path of the room to which it
                belongs
                """
                sensor_observation_files = os.listdir(self.path)
                indexes = [i for i, j in enumerate(sensor_observation_files) if j.split('_')[0] == self.id]
                """
                If files is empty the file names are loaded
                If not, file names are already loaded (cached)
                """
                if len(self.files) == 0:
                    for i in indexes:
                        self.files.append(sensor_observation_files[i])
                    """
                    According to some files features self instance is casted
                    to a specialized one.
                    """
                    if 'scan' in sensor_observation_files[i]:
                        self.__class__ = Dataset.DatasetUnitRawData.SensorLaserScanner
                    else:
                        self.__class__ = Dataset.DatasetUnitRawData.SensorCamera

                return self.files.sort()

            def get_type(self):
                """
                Example:
                with a type like this:
                <class '__main__.Dataset.DatasetUnitRawData.SensorCamera'>
                return this:
                SensorCamera
                """
                return str(type(self)).split('.')[-1][:-2]

        class Sensors(list):
            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Sensors list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class SensorCamera(Sensor):
            def __init__(self, id='0', name='undefined',
                         sensor_pose_x='0', sensor_pose_y='0', sensor_pose_z='0',
                         sensor_pose_yaw='0', sensor_pose_pitch='0', sensor_pose_roll='0',
                         time_stamp='0', files=[]):
                """ Calls the super class __init__"""
                super().__init__(id, name,
                                 sensor_pose_x, sensor_pose_y, sensor_pose_z,
                                 sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll,
                                 time_stamp, files)

            def __str__(self):
                s = '\t' + 'Camera: '
                return s + super().__str__()

            def __repr__(self):
                s = "<SensorCamera instance (" + self.name + ")>"
                return s

            def get_depth_file(self):
                index = [i for i, j in enumerate(self.files) if 'depth' in j]
                return self.path + '/' + self.files[index[0]]

            def get_intensity_file(self):
                index = [i for i, j in enumerate(self.files) if 'intensity' in j]
                return self.path + '/' + self.files[index[0]]

            def get_labels_file(self):
                index = [i for i, j in enumerate(self.files) if 'labels' in j]
                return self.path + '/' + self.files[index[0]]

            def get_intensity_image(self):
                intensity_file = self.get_intensity_file()
                img = cv2.imread(intensity_file, cv2.IMREAD_COLOR)
                img_rot = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                return img_rot

            def get_depth_image(self):
                depth_file = self.get_depth_file()
                img = cv2.imread(depth_file, cv2.IMREAD_COLOR)
                img_rot = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                return img_rot

            def get_labels(self):
                labels = Dataset.DatasetUnitRawData.Labels()
                labels_file = self.get_labels_file()
                labels_file_path = labels_file
                with open(labels_file_path, "r") as file_handler:
                    line = file_handler.readline()
                    while line:
                        words = line.strip().split()
                        if words[0][0] != '#':
                            num_of_labels = int(words[0])
                            break
                        line = file_handler.readline()
                    #print('num_of_labels: ' + str(num_of_labels))

                    for i in range(num_of_labels):
                        line = file_handler.readline()
                        words = line.strip().split()
                        # print(words)
                        label = Dataset.DatasetUnitRawData.Label(words[0],
                                                                 words[1])
                        labels.append(label)

                return labels

            def __get_mask(self):
                mask = []
                labels_file = self.get_labels_file()
                labels_file_path = labels_file
                with open(labels_file_path, "r") as file_handler:
                    line = file_handler.readline()
                    while line:
                        words = line.strip().split()
                        if words[0][0] != '#':
                            num_of_labels = int(words[0])
                            break
                        line = file_handler.readline()

                    for i in range(num_of_labels):
                        line = file_handler.readline()
                        words = line.strip().split()

                    num_of_rows = 0
                    line = file_handler.readline()
                    while line:
                        num_of_rows += 1
                        words = line.strip().split()
                        mask.append(list(map(int, words)))
                        line = file_handler.readline()
                # h = len(mask)
                # w = len(mask[0])

                return mask

            def get_label_mask(self, pos):
                mask = self.__get_mask()
                arr = np.array(mask)
                arr = np.rot90(arr)
                arr = arr & (2**(pos))
                np.clip(arr, 0, 1, out=arr)
                arr = np.uint8(arr)
                arr = arr * 255
                return arr

            def show_intensity_image(self):
                img = self.get_intensity_image()
                cv2.imshow("Intensity image " + "#" + self.id, img)
                if img is None:
                    sys.exit("Could not read the image.")

            def show_depth_image(self):
                img = self.get_depth_image()
                cv2.imshow("Depth image" + "#" + self.id, img)
                if img is None:
                    sys.exit("Could not read the image.")

            def show_label_mask_image(self, pos):
                img = self.get_label_mask(pos)
                cv2.imshow("Label mask" + "#" + self.id +
                           ' label: ' + str(pos), img)
                if img is None:
                    sys.exit("Could not read the image.")

        class SensorCameras(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<SensorCameras list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class SensorLaserScanner(Sensor):
            def __init__(self, id='0', name='undefined',
                         sensor_pose_x='0', sensor_pose_y='0', sensor_pose_z='0',
                         sensor_pose_yaw='0', sensor_pose_pitch='0', sensor_pose_roll='0',
                         time_stamp='0', files=[]):
                """ Calls the super class __init__"""
                super().__init__(id, name,
                                 sensor_pose_x, sensor_pose_y, sensor_pose_z,
                                 sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll,
                                 time_stamp, files)

            def __str__(self):
                s = '\t' + 'Laser scanner: '
                return s + super().__str__()

            def __repr__(self):
                s = "<SensorLaserScanner instance (" + self.name + ")>"
                return s

            def get_laser_scan_bak(self, path):
                laser_scan = Dataset.DatasetUnitRawData.LaserScan()
                with open(path + '/' + self.files[0], "r") as file_handler:
                    line_number = 0
                    for line in file_handler:
                        words = line.strip().split()
                        if words[0] != '#':
                            line_number += 1
                            if line_number == 1:
                                laser_scan.aperture = words[0]
                            elif line_number == 2:
                                laser_scan.max_range = words[0]
                            elif line_number == 4:
                                laser_scan.vector_of_scans = words
                            elif line_number == 5:
                                laser_scan.vector_of_valid_scans = words
                return laser_scan

            def get_laser_scan(self):
                laser_scan = Dataset.DatasetUnitRawData.LaserScan()
                with open(self.path + '/' + self.files[0], "r") as file_handler:
                    line_number = 0
                    for line in file_handler:
                        words = line.strip().split()
                        if words[0] != '#':
                            line_number += 1
                            if line_number == 1:
                                laser_scan.aperture = words[0]
                            elif line_number == 2:
                                laser_scan.max_range = words[0]
                            elif line_number == 4:
                                laser_scan.vector_of_scans = words
                            elif line_number == 5:
                                laser_scan.vector_of_valid_scans = words
                return laser_scan

        class SensorLaserScanners(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<SensorLaserScanners list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class LaserScan():
            def __init__(self, aperture='0', max_range='0',
                         vector_of_scans=[], vector_of_valid_scans=[]):
                self.aperture = aperture
                self.max_range = max_range
                self.vector_of_scans = vector_of_scans
                self.vector_of_valid_scans = vector_of_valid_scans

            def __str__(self):
                s = '\t' + 'Laser scan: ' +  self.aperture + ', ' + \
                    self.max_range + ', num. of scans: ' + \
                    str(len(self.vector_of_scans)) + ', valid: ' + \
                    str(len(self.vector_of_valid_scans))
                return s

            def __repr__(self):
                s = "<LaserScan instance (" + self.name + ")>"
                return s

        class LaserScans(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<LaserScans list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class Label():
            def __init__(self, id='', name=''):
                self.id = id
                self.name = name

            def __str__(self):
                s = '\t' + 'Label: ' +  self.id + ', ' + self.name
                return s

            def __repr__(self):
                s = "<Label instance (" + self.name + ")>"
                return s

        class Labels(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Labels list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [label.name for label in self]

            def get_ids(self):
                return [label.id for label in self]

            def as_dict_id(self):
                keys = [label.id for label in self]
                zip_obj = zip(keys, self)
                new_dict = dict(zip_obj)
                return new_dict

            def as_dict_name(self):
                keys = [label.name for label in self]
                zip_obj = zip(keys, self)
                new_dict = dict(zip_obj)
                return new_dict

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)

        def _load_function(self):
            self.home_sessions = self.HomeSessions()
            home_folders = sorted(os.listdir(self.path))
            # print(home_folders)
            for home_folder in home_folders:
                words = home_folder.strip().split('-')
                len_of_words = len(words)
                home_subfolder = words[len_of_words-2] + '-' + \
                                 words[len_of_words-1]
                rooms = self.Rooms()
                room_files = sorted(os.listdir(self.path + '/' +
                                               home_folder + '/' +
                                               home_subfolder))
                room_relative_path = (
                    self.path.split('/')[-1] + '/' +
                    home_folder + '/' +
                    home_subfolder
                )
                # print(room_files)
                for room_file in room_files:
                    if room_file.endswith('.txt'):
                        #print(room_file)
                        room_folder_path = self.path + '/' + home_folder + \
                                           '/' + home_subfolder + '/' + \
                                           room_file.split('.')[0]
                        room_file_path = self.path + '/' + home_folder + \
                                         '/' + home_subfolder + '/' + \
                                         room_file
                        sensors = self.Sensors()
                        # print(sensor_observations_files)
                        with open(room_file_path, "r") as file_handler:
                            for line in file_handler:
                                words = line.strip().split()
                                if words[0] != '#':
                                    """
                                    Read a line with the following structure:
                                    words  0 : [Observation_id]
                                    words  1 : [sensor_label]
                                    words  2 : [sensor_pose_x]
                                    words  3 : [sensor_pose_y]
                                    words  4 : [sensor_pose_z]
                                    words  5 : [sensor_pose_yaw]
                                    words  6 : [sensor_pose_pitch]
                                    words  7 : [sensor_pose_roll]
                                    words  8 : [time-stamp]
                                    """
                                    # print(words[0])
                                    sensor = self.Sensor(words[0],
                                                         words[1],
                                                         words[2],
                                                         words[3],
                                                         words[4],
                                                         words[5],
                                                         words[6],
                                                         words[7],
                                                         words[8],
                                                         [],
                                                         room_folder_path,
                                                         room_relative_path + "/" + room_file.split('.')[0])
                                    sensors.append(sensor)
                        room = self.Room(room_file.split('.')[0],
                                         room_folder_path,
                                         sensors)
                        rooms.append(room)
                        # print(room)
                # print(rooms)
                # input("Press Enter to continue...")
                home_session = self.HomeSession(home_subfolder, rooms)
                self.home_sessions.append(home_session)
            # return home_sessions

        def __str__(self):
            s = ""
            for self.home_session in self.home_sessions:
                s += self.home_session.name + "\n"
                for self.room in self.home_session.rooms:
                    s += "\t" + self.room.name + " (" + str(len(self.room.sensor_observations)) + " observations)" + "\n"
            return super().__str__() + s

    class DatasetUnitLaserScans(DatasetUnit):
        class HomeSession():
            def __init__(self, name, rooms):
                self.name = name
                self.rooms = rooms

            def __str__(self):
                s = '\t' + self.name
                return s

            def __repr__(self):
                s = "<HomeSession instance (" + self.name + ")>"
                return s

            def get_home_name(self):
                return self.name.split('-s')[0]

        class HomeSessions(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<HomesSessions list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [home.name for home in self]

        class Room():
            def __init__(self, name, folder_path, sensor_sessions):
                self.name = name
                self.folder_path = folder_path
                self.sensor_sessions = sensor_sessions

            def __str__(self):
                s = '\t' + self.name + '  folder: /' + self.folder_path + \
                    ' # sensor_sessions: ' + str(len(self.sensor_sessions))
                return s

            def __repr__(self):
                s = "<Room instance (" + self.name + ")>"
                return s

        class Rooms(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Rooms list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class SensorSession():
            def __init__(self, name, folder_path, sensor_observations):
                self.name = name
                self.folder_path = folder_path
                self.sensor_observations = sensor_observations

            def __str__(self):
                s = '\t' + self.name + '  folder: /' + self.folder_path + \
                    ' # observations: ' + str(len(self.sensor_observations))
                return s

            def __repr__(self):
                s = "<SensorSession instance (" + self.name + ")>"
                return s

        class SensorSessions(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<SensorSessions list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class Sensor():
            def __init__(self, id='0', name='undefined',
                         sensor_pose_x='0', sensor_pose_y='0', sensor_pose_z='0',
                         sensor_pose_yaw='0', sensor_pose_pitch='0', sensor_pose_roll='0',
                         time_stamp='0', files=[], path="", rel_path=""):
                self.id = id
                self.name = name
                self.sensor_pose_x = sensor_pose_x
                self.sensor_pose_y = sensor_pose_y
                self.sensor_pose_z = sensor_pose_z
                self.sensor_pose_yaw = sensor_pose_yaw
                self.sensor_pose_pitch = sensor_pose_pitch
                self.sensor_pose_roll = sensor_pose_roll
                self.time_stamp = time_stamp
                self.files = files
                self.path = path
                self.rel_path = rel_path

            def __str__(self):
                s = '\t' + self.id + ', ' + self.name + ', ' + \
                    self.sensor_pose_x + ', ' + \
                    self.sensor_pose_y + ', ' + \
                    self.sensor_pose_z + ', ' + \
                    self.sensor_pose_yaw + ', ' + \
                    self.sensor_pose_pitch + ', ' + \
                    self.sensor_pose_roll + ', ' + \
                    self.time_stamp + ', ' + \
                    str(self.files)
                return s

            def __repr__(self):
                s = "<Sensor instance (" + self.name + ")>"
                return s

            def load_files(self):

                """
                The path should be the room.path of the room to which it
                belongs
                """
                sensor_observation_files = os.listdir(self.path)
                indexes = [i for i, j in enumerate(sensor_observation_files) if j.split('_')[0] == self.id]
                """
                If files is empty the file names are loaded
                If not, file names are already loaded (cached)
                """
                if len(self.files) == 0:
                    for i in indexes:
                        self.files.append(sensor_observation_files[i])
                    """
                    According to some files features self instance is casted
                    to a specialized one.
                    """
                    if 'scan' in sensor_observation_files[i]:
                        self.__class__ = Dataset.DatasetUnitLaserScans.SensorLaserScanner

                return self.files

            def get_type(self):
                """
                Example:
                with a type like this:
                <class '__main__.Dataset.DatasetUnitRawData.SensorCamera'>
                return this:
                SensorCamera
                """
                return str(type(self)).split('.')[-1][:-2]

        class Sensors(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Sensors list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class SensorLaserScanner(Sensor):
            def __init__(self, id='0', name='undefined',
                         sensor_pose_x='0', sensor_pose_y='0', sensor_pose_z='0',
                         sensor_pose_yaw='0', sensor_pose_pitch='0', sensor_pose_roll='0',
                         time_stamp='0', files=[]):
                """ Calls the super class __init__"""
                super().__init__(id, name,
                                 sensor_pose_x, sensor_pose_y, sensor_pose_z,
                                 sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll,
                                 time_stamp, files)

            def __str__(self):
                s = '\t' + 'Laser scanner: '
                return s + super().__str__()

            def __repr__(self):
                s = "<SensorLaserScanner instance (" + self.name + ")>"
                return s

            def get_laser_scan(self):
                laser_scan = Dataset.DatasetUnitLaserScans.LaserScan()
                with open(self.path + '/' + self.files[0], "r") as file_handler:
                    line_number = 0
                    for line in file_handler:
                        words = line.strip().split()
                        if words[0] != '#':
                            line_number += 1
                            if line_number == 1:
                                laser_scan.aperture = words[0]
                            elif line_number == 2:
                                laser_scan.max_range = words[0]
                            elif line_number == 4:
                                laser_scan.vector_of_scans = words
                            elif line_number == 5:
                                laser_scan.vector_of_valid_scans = words
                return laser_scan

        class SensorLaserScanners(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<SensorLaserScanners list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class LaserScan():
            def __init__(self, aperture='0', max_range='0',
                         vector_of_scans=[], vector_of_valid_scans=[]):
                self.aperture = aperture
                self.max_range = max_range
                self.vector_of_scans = vector_of_scans
                self.vector_of_valid_scans = vector_of_valid_scans

            def __str__(self):
                s = '\t' + 'Laser scan: ' +  self.aperture + ', ' + \
                    self.max_range + ', num. of scans: ' + \
                    str(len(self.vector_of_scans)) + ', valid: ' + \
                    str(len(self.vector_of_valid_scans))
                return s

            def __repr__(self):
                s = "<LaserScan instance (" + self.name + ")>"
                return s

        class LaserScans(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<LaserScans list instance (" + str(len(self)) + \
                    " items)>"
                return s

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)

            # self.home_sessions = self.__load_data()

        def _load_function(self):
            home_folders = sorted(os.listdir(self.path))
            self.home_sessions = self.HomeSessions()
            # print(home_folders)
            for home_folder in home_folders:
                words = home_folder.strip().split('-')
                len_of_words = len(words)
                home_subfolder = words[len_of_words-2] + '-' + \
                                 words[len_of_words - 1]
                # print(home_folder)
                room_folders = sorted(os.listdir(self.path + '/' +
                                                 home_folder + '/' +
                                                 home_subfolder))
                room_relative_path = (
                    self.path.split('/')[-1] + '/' +
                    home_folder + '/' +
                    home_subfolder
                )
                # print(room_folders)
                rooms = self.Rooms()
                for room_folder in room_folders:
                    # print(room_folder)
                    room_folder_path = self.path + '/' + home_folder + \
                                       '/' + home_subfolder + '/' + \
                                       room_folder
                    sensor_session_files = sorted(os.listdir(room_folder_path))
                    # print(sensor_session_files)
                    sensor_sessions = self.SensorSessions()
                    for sensor_session_file in sensor_session_files:
                        if sensor_session_file.endswith('.txt'):
                            # print(sensor_session_file)
                            sensor_session_folder_path = room_folder_path + '/' + \
                                               sensor_session_file.split('.')[0]
                            sensor_session_file_path = room_folder_path + '/' + \
                                               sensor_session_file
                            # print(sensor_session_folder_path)
                            # print(sensor_session_file_path)
                            sensors = self.Sensors()
                            with open(sensor_session_file_path, "r") as file_handler:
                                for line in file_handler:
                                    words = line.strip().split()
                                    if words[0] != '#':
                                        """
                                        Read a line with the following structure:
                                        words  0 : [Observation_id]
                                        words  1 : [sensor_label]
                                        words  2 : [sensor_pose_x]
                                        words  3 : [sensor_pose_y]
                                        words  4 : [sensor_pose_z]
                                        words  5 : [sensor_pose_yaw]
                                        words  6 : [sensor_pose_pitch]
                                        words  7 : [sensor_pose_roll]
                                        words  8 : [time-stamp]
                                        """
                                        # print(words[0])
                                        sensor = self.Sensor(words[0],
                                                             words[1],
                                                             words[2],
                                                             words[3],
                                                             words[4],
                                                             words[5],
                                                             words[6],
                                                             words[7],
                                                             words[8],
                                                             [],
                                                             sensor_session_folder_path,
                                                             room_relative_path + "/" + room_folder + "/" + sensor_session_file.split('.')[0]
                                                             )
                                        sensors.append(sensor)
                            sensor_session = self.SensorSession(sensor_session_file.split('.')[0],
                                                                sensor_session_folder_path, sensors)
                            sensor_sessions.append(sensor_session)
                    room = self.Room(room_folder,
                                     room_folder_path, sensor_sessions)
                    rooms.append(room)
                    # print(room)
                # print(rooms)
                # input("Press Enter to continue...")
                home_session = self.HomeSession(home_subfolder, rooms)
                self.home_sessions.append(home_session)

            # return home_sessions

        def __str__(self):
            s = ""
            s = ""
            for self.home_session in self.home_sessions:
                s += self.home_session.name + "\n"
                for self.room in self.home_session.rooms:
                    s += "\t" + self.room.name + " (" + str(len(self.room.sensor_sessions)) + " sessions)" + "\n"
                    for self.sensor_session in self.room.sensor_sessions:
                        s += "\t\t" + self.sensor_session.name + " (" + str(len(self.sensor_session.sensor_observations)) + " observations)" + "\n"
            return super().__str__() + s

    class DatasetUnitSceneData(DatasetUnit):
        class HomeSession():
            def __init__(self, name, rooms):
                self.name = name
                self.rooms = rooms

            def __str__(self):
                s = '\t' + self.name
                return s

            def __repr__(self):
                s = "<HomeSession instance (" + self.name + ")>"
                return s

            def get_home_name(self):
                return self.name.split('-s')[0]

        class HomeSessions(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<HomesSessions list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [home.name for home in self]

        class Room():
            def __init__(self, name, scene_file, boundingboxes):
                self.name = name
                self.scene_file = scene_file
                self.boundingboxes = boundingboxes

            def __str__(self):
                s = '\t' + self.name + '  folder: /' + self.folder_path + \
                    ' boundingboxes: ' + str(len(self.boundingboxes))
                return s

            def __repr__(self):
                s = "<Room instance (" + self.name + ")>"
                return s

        class Rooms(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<Rooms list instance (" + str(len(self)) + \
                    " items)>"
                return s

        class BoundingBox():

            def __init__(self, id='0', name='undefined',
                         bb_pose=[0.0]*6,
                         bb_corner=[0.0]*6):
                self.id = id
                self.name = name
                self.bb_pose = bb_pose
                self.bb_corner = bb_corner

            def __str__(self):
                s = '\t' + self.id + ', ' + self.name + ', ' + \
                    str(self.bb_pose) + ', ' + \
                    str(self.bb_corner)
                return s


            def __repr__(self):
                s = "<BoundingBox instance (" + self.name + ")>"
                return s

        class BoundingBoxes(list):

            def __init__(self):
                pass

            def __str__(self):
                s = ''
                for item in self:
                    s += str(item) + "\n"
                return s

            def __repr__(self):
                s = "<BoundingBox list instance (" + str(len(self)) + \
                    " items)>"
                return s

            def get_names(self):
                return [bounding_box.name for bounding_box in self]

            def get_ids(self):
                return [bounding_box.id for bounding_box in self]

            def get_boundingbox_pose(self):
                return self.bb_pose

            def get_boundingbox_corner(self):
                return self.bb_corner

            def as_dict_id(self):
                keys = [bounding_box.id for bounding_box in self]
                zip_obj = zip(keys, self)
                new_dict = dict(zip_obj)
                return new_dict

            def as_dict_name(self):
                keys = [bounding_box.name for bounding_box in self]
                zip_obj = zip(keys, self)
                new_dict = dict(zip_obj)
                return new_dict

        def __init__(self, name="", url="", path="", expected_hash_code="",
                     expected_size=0):
            """ Calls the super class __init__"""
            super().__init__(name, url, path, expected_hash_code,
                             expected_size)

        def _load_function(self):
            self.home_sessions = self.HomeSessions()
            home_folders = sorted(os.listdir(self.path))
            for home_folder in home_folders:
                words = home_folder.strip().split('_')
                len_of_words = len(words)
                home_subfolder = words[len_of_words - 1]
                room_relative_path = (
                    self.path.split('/')[-1] + '/' +
                    home_folder + '/' +
                    home_subfolder
                )
                room_folder = self.path + '/' + home_folder + '/' + home_subfolder
                rooms = self.Rooms()
                room_files = sorted(os.listdir(room_folder))
                for room_file in room_files:
                    boundingboxes = self.BoundingBoxes()
                    room_file_path = room_folder + '/' + room_file
                    with open(room_file_path, "r") as file_handler:
                        num_of_boundingboxes = 0
                        num_of_header_lines = 0
                        line = file_handler.readline()
                        while line[0] == '#':
                            num_of_header_lines += 1
                            line = file_handler.readline()
                        # The header belongs to a file with bounding boxes.
                        # There is another type of header with 5 lines and
                        # no bounding boxes.
                        if num_of_header_lines == 13:
                            words = line.strip().split()
                            num_of_boundingboxes = words[0]
                            for bb_id in range(int(num_of_boundingboxes)):
                                line = file_handler.readline()
                                words = line.strip().split()
                                object_name = words[0]
                                # [bb_pose_x] [bb_pose_y] [bb_pose_z] [bb_pose_yaw] [bb_pose_pitch] [bb_pose_roll]
                                line = file_handler.readline()
                                bb_pose = line.strip().split()
                                # [bb_corner1_x] [bb_corner1_y] [bb_corner1_z]
                                line = file_handler.readline()
                                bb_corner1 = line.strip().split()
                                # [bb_corner2_x] [bb_corner2_y] [bb_corner2_z]
                                line = file_handler.readline()
                                bb_corner2 = line.strip().split()
                                boundingbox = self.BoundingBox(bb_id,
                                                               object_name,
                                                               bb_pose,
                                                               bb_corner1 + bb_corner2
                                                               )
                                boundingboxes.append(boundingbox)
                    room_name = room_file.rsplit('_', 1)[0]
                    room_name = room_name.split('_labelled')[0]
                    # if '_labelled' in room.name:
                    #     room_name = room.name.split('_labelled_scene')[0]
                    # else:
                    #     room_name = room.name.split('_scene')[0]
                    # breakpoint()
                    room = self.Room(room_name,
                                     room_relative_path + '/' + room_file, #room_file_path,
                                     boundingboxes)
                    rooms.append(room)
                home_session = self.HomeSession(home_subfolder, rooms)
                self.home_sessions.append(home_session)

        def __str__(self):
            s = ""
            for self.home_session in self.home_sessions:
                s += self.home_session.name + "\n"
                for self.room in self.home_session.rooms:
                    s += "\t" + self.room.name + " (" + str(len(self.room.boundingboxes)) + " bounding boxes)" + "\n"
            return super().__str__() + s


    # @profile
    def __init__(self,
                 name="",
                 path=os.path.abspath("."),
                 url="",
                 autoload="True"):

        """
        Robot@Home Dataset
        """

        self.name = name
        self.path = path
        self.url = url
        self.autoload = autoload

        print (version.get_version_str())

        self.unit = {}


        self.unit["chelmnts"] = self.DatasetUnitCharacterizedElements(
            "Characterized elements",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_characterized-elements"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_characterized-elements.tgz?download=1",
            "2b4d99dd258e619bf53d7cf7cbf9843c",
            31450784)

        self.unit["2dgeomap"] = self.DatasetUnit2DGeometricMaps(
            "2D geometric maps",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_2d_geometric_maps"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_2d_geometric_maps.tgz?download=1",
            "cf622ee997bc620e297bff8d3a2491d3",
            8240734)

        self.unit["hometopo"] = self.DatasetUnitHomesTopologies(
            "Home's topologies",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_homes-topologies"),
           "https://zenodo.org/record/4495821/files/Robot@Home-dataset_homes-topologies.tgz?download=1",
           "78f65c424099fb6a040b43d65166fc7d",
            41019)

        self.unit["raw"] = self.DatasetUnitRawData(
            "Raw data",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_raw_data-plain_text-all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_raw_data-plain_text-all.tgz?download=1",
            "5d14ceed9a84fb0016bf2144df8f3efb",
            20002442369)

        self.unit["lsrscan"] = self.DatasetUnitLaserScans(
            "Laser scans",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_laser_scans-plain_text-all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_laser_scans-plain_text-all.tgz?download=1",
            "61b7a671a843355dcf7c2ba80bed6c45",
            227829791)

        self.unit["rgbd"] = self.DatasetUnitRawData(
            "RGB-D data",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_rgbd_data-plain_text-all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_rgbd_data-plain_text-all.tgz?download=1",
            "1d3218acd80aa88c66f713ffdb2bd4d4",
            19896608308)

        self.unit["lblrgbd"] = self.DatasetUnitRawData(
            "Labelled RGB-D data",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_labelled-rgbd-data_plain-text_all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_labelled-rgbd-data_plain-text_all.tgz?download=1",
            "8165eefb59dbacc5faa539ad4ab3080e",
            16739353847)

        self.unit["lblscene"] = self.DatasetUnitSceneData(
            "Labelled scene data",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_labelled-scenes_plain-text_all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_labelled-scenes_plain-text_all.tgz?download=1",
            "17342b5bcdd37845bf772ebd32905c59",
            7947369064)

        self.unit["rctrscene"] = self.DatasetUnitSceneData(
            "Reconstructed scene data",
            os.path.abspath(self.path + "/" + "Robot@Home-dataset_reconstructed-scenes_plain-text_all"),
            "https://zenodo.org/record/4495821/files/Robot@Home-dataset_reconstructed-scenes_plain-text_all.tgz?download=1",
            "cdcd1a41f47f17e823b4c9f46737ff91",
            7947563808)



        if self.autoload:
            self.unit["chelmnts"].load_data()
            self.unit["2dgeomap"].load_data()
            self.unit["hometopo"].load_data()
            self.unit["raw"].load_data()
            self.unit["lsrscan"].load_data()
            self.unit["rgbd"].load_data()
            self.unit["lblrgbd"].load_data()
            self.unit["lblscene"].load_data()
            self.unit["rctrscene"].load_data()

            """
            Memory profile
            2737    102.3 MiB      0.0 MiB           if self.autoload:
            2738    557.0 MiB    454.8 MiB               self.unit["chelmnts"].load_data()
            2739    661.8 MiB    104.7 MiB               self.unit["2dgeomap"].load_data()
            2740    661.9 MiB      0.2 MiB               self.unit["hometopo"].load_data()
            2741    714.8 MiB     52.9 MiB               self.unit["raw"].load_data()
            2742    741.9 MiB     27.1 MiB               self.unit["lsrscan"].load_data()
            2743    784.4 MiB     42.5 MiB               self.unit["rgbd"].load_data()
            2744    812.9 MiB     28.5 MiB               self.unit["lblrgbd"].load_data()
            Total                710.7 MiB
            """


    def __str__(self):

        """ Units """

        total_expected_size = 0

        s = "\n" + self.name + " Dataset Units" + "\n" + "=" * len(self.name+" Dataset Units") +"\n"*2
        # s += "Units" + "\n" + "=====" + "\n"*2
        for index, unit in self.unit.items():
            s += index + " : " + unit.name + " "
            if unit.__data_loaded__:
                s += "(expected " + humanize.naturalsize(unit.expected_size) + ")\n"
            else:
                s += "(unloaded)\n"
            #s += unit.__str__()
            total_expected_size += unit.expected_size

        s += "\n"
        s += 'Total expected size on disk = ' + str(total_expected_size) + " bytes"\
             ' (' + humanize.naturalsize(total_expected_size) + ')'
        s += "\n"


        return s


def main():
    print (version.get_version_str())

    return 0


if __name__ == "__main__":
    main()
