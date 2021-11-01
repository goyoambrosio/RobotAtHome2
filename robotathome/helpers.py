#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/22"
__license__ = "MIT"

import os
import datetime as dt
import time
import re
import hashlib
import tarfile
import io
import sys
import requests
from tqdm.auto import tqdm
from .log import logger

__all__ = ['download', 'get_md5', 'uncompress',
           'flat2Dlist', 'flatlist', 'reverse_dict',
           'time_win2unixepoch', 'time_unixepoch2win',
           'rename_if_exist'
           ]

"""
Helper functions
"""

# Download related

def download(url: str, path: str = os.getcwd()) -> None:
    """
    Download file with progressbar

    Args:
        url: a hyperlink that points to a location where the file to download
    resides.
        path: path where the file will be stored

    Example:
        >>> import robotathome as rh
        >>> rh.download('https://...','~/Download')
    """
    # if not filename:
    #     local_filename = os.path.join(".", url.split('/')[-1])
    # else:
    #     local_filename = filename

    # print("Unexpected error: ",sys.exc_info()[0], " occurred.")

    req = requests.get(url, stream=True)
    logger.debug("Status code: {}", req.status_code)

    try:
        req.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.info("The file couldn\'t be retrieved")
        logger.error("Error: {}", error)
        # Whoops it wasn't a 200
        # return "Error: " + error
    else:
        if (os.path.isdir(os.path.expanduser(path))):
            remote_filename = req.headers.get("Content-Disposition").split("filename=")[1]
            logger.debug("remote_filename: {}", remote_filename)
            local_filename = os.path.expanduser(os.path.join(path, remote_filename.strip(' " " ')))
            logger.debug("local_filename: {}", local_filename)
            file_size = int(req.headers['Content-Length'])
            chunk = 1
            chunk_size = 2**20 # 1024 for KB, 1024*1024 for MB
            num_bars = int(file_size / chunk_size)
            try:
                with open(local_filename, 'wb') as fp:
                    for chunk in tqdm(req.iter_content(chunk_size=chunk_size),
                                      total=num_bars,
                                      unit='MB',
                                      # unit_scale=1,
                                      # unit_divisor=2**10,
                                      desc=local_filename,
                                      leave=True  # progressbar stays
                                      ):
                        fp.write(chunk)
                logger.info('Sucessfully downloaded: {}', local_filename)
            except Exception as error:
                logger.error("Error: {}", error)
                logger.info('Something went wrong trying to download {}', local_filename)
            finally:
                fp.close()

        else:
            logger.error("Error: The directory {} doesn\'t exist", path)
            logger.info("The file couldn\'t be retrieved")

def get_md5(filename: str) -> str:
    """Computes MD5 hash of a given file

    Args:
        filename: the filename to get the md5 hash

        path: the path where the filename is located

    Returns:
        a string with the MD5 hash value
    """

    try:
        local_filename = os.path.expanduser(filename)
        chunk_size = 65536
        hasher = hashlib.md5()
        with open(local_filename, 'rb') as afile:
            buf = afile.read(chunk_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(chunk_size)
        logger.debug("MD5 checksum for {} : {}",
                        local_filename,
                        hasher.hexdigest()
                        )
        return hasher.hexdigest()
    except Exception as error:
        logger.error("Error: {}", error)
        return ''

def uncompress(filename: str, path: str = os.getcwd()) -> None:
    """Uncompress a tar file

       Args:
           filename: a tar file (tar, tgz, ...)
           path: where the filename will be uncompressed

    Example:
        >>> import robotathome as rh
        >>> rh.uncompress('~/WORKSPACE/Robot@Home2_db.tgz')
    """
    class ProgressFileObject(io.FileIO):
        def __init__(self, path, *args, **kwargs):
            self._total_size = os.path.getsize(path)
            io.FileIO.__init__(self, path, *args, **kwargs)

        def read(self, size):
            sys.stdout.write("\rUncompressing %d of %d MB (%d%%)" % (self.tell() / 1048576, self._total_size / 1048576, self.tell()*100/self._total_size))
            sys.stdout.flush()
            return io.FileIO.read(self, size)

    try:
        logger.info("Extracting files from {}: ", (os.path.basename(filename)))
        file_obj=ProgressFileObject(os.path.expanduser(filename))
        tf = tarfile.open(fileobj=file_obj)
        tf.extractall(path=os.path.expanduser(path))
        file_obj.close()
    except Exception as error_code:
        logger.info("Error: {}", error_code)
    else:
        tf.close()
        print()
        logger.info("Extraction success. Don't forget to remove {} if you are not plenty of space.",
                       (os.path.basename(filename)))


# Misc

def flat2Dlist(list_):
    return sum(list_, [])

def flatlist(list_):
    if len(list_) == 0:
        return list_
    if isinstance(list_[0], list):
        return flatlist(list_[0]) + flatlist(list_[1:])
    return list_[:1] + flatlist(list_[1:])

def reverse_dict(dict_):
    return dict(map(reversed, dict_.items()))


# Time

def time_win2unixepoch(time_stamp):
    ''' Doctring '''
    seconds = time_stamp / 10000000
    epoch = seconds - 11644473600
    datetime_ = dt.datetime(2000, 1, 1, 0, 0, 0)
    return datetime_.fromtimestamp(epoch)

def time_unixepoch2win(date):
    ''' Doctring '''
    match = re.compile(r'^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)$').match(date)
    if match:
        datetime_ = dt.datetime(*map(int, match.groups()))
        windows_timestamp = (time.mktime(datetime_.timetuple()) + 11644473600) * 10000000
    else:
        logger.error("Invalid date format specified: {}\n Specify a date and time string in the format: \"yyyy-MM-ddTHH:mm:ss\"")
        windows_timestamp = 0
    return windows_timestamp

# Log

def rename_if_exist(file_name, tail='.bak'):
    if os.path.isfile(file_name):
        logger.warning("This file name already exists. Adding .bak")
        new_file_name = file_name + tail
        os.rename(file_name, new_file_name)

# Lab
