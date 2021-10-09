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
from tqdm.autonotebook import tqdm
# import tqdm
# from tqdm import tqdm
import numpy as np
import cv2
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import mxnet as mx
import gluoncv as gcv
import pandas as pd
import robotathome as rh


"""
Getting dataset
"""

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
    rh.logger.debug("Status code: {}", req.status_code)

    try:
        req.raise_for_status()
    except requests.exceptions.RequestException as error:
        rh.logger.info("The file couldn\'t be retrieved")
        rh.logger.error("Error: {}", error)
        # Whoops it wasn't a 200
        # return "Error: " + error
    else:
        if (os.path.isdir(os.path.expanduser(path))):
            remote_filename = req.headers.get("Content-Disposition").split("filename=")[1]
            rh.logger.debug("remote_filename: {}", remote_filename)
            local_filename = os.path.expanduser(os.path.join(path, remote_filename.strip(' " " ')))
            rh.logger.debug("local_filename: {}", local_filename)
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
                rh.logger.info('Sucessfully downloaded: {}', local_filename)
            except Exception as error:
                rh.logger.error("Error: {}", error)
                rh.logger.info('Something went wrong trying to download {}', local_filename)
            finally:
                fp.close()

        else:
            rh.logger.error("Error: The directory {} doesn\'t exist", path)
            rh.logger.info("The file couldn\'t be retrieved")

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
        rh.logger.debug("MD5 checksum for {} : {}",
                        local_filename,
                        hasher.hexdigest()
                        )
        return hasher.hexdigest()
    except Exception as error:
        rh.logger.error("Error: {}", error)
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
        rh.logger.info("Extracting files from {}: ", (os.path.basename(filename)))
        file_obj=ProgressFileObject(os.path.expanduser(filename))
        tf = tarfile.open(fileobj=file_obj)
        tf.extractall(path=os.path.expanduser(path))
        file_obj.close()
    except Exception as error_code:
        rh.logger.info("Error: {}", error_code)
    else:
        tf.close()
        print()
        rh.logger.info("Extraction success. Don't forget to remove {} if you are not plenty of space.",
                       (os.path.basename(filename)))


"""
misc
"""

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

def overlay_mask(img, masks, alpha=0.5):
    # cv2.addWeighted(ovl_img, alpha, base_img, 1 - alpha, 0, base_img)
    # return base_img
    colors = []
    for mask in masks:
        color = np.random.random(3)
        colors.append(np.append(color,[alpha]))
        mask = np.repeat((mask > 0)[:, :, np.newaxis], repeats=3, axis=2)
        img = np.where(mask, img * (1 - alpha) + color*255 * alpha, img)
    return img.astype('uint8'), colors

def plot_mask(patched_img, names, colors):
    plt.imshow(patched_img)
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    mpatches_=[]
    for i, color_ in enumerate(colors):
        mpatches_.append(mpatches.Patch(color=color_, label=names[i]))
    plt.legend(handles=mpatches_)
    plt.show()


"""
time
"""

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
        print("Invalid date format specified: " + date)
        print("Specify a date and time string in the format: \"yyyy-MM-ddTHH:mm:ss\"")
        windows_timestamp = 0
    return windows_timestamp


"""
log
"""

def get_log_levels():
    log_levels_key_no = {}
    level_values = rh.logger._core.levels.values()
    for level_value in level_values:
        log_levels_key_no[level_value.no] = level_value.name
    log_levels_key_name = reverse_dict(log_levels_key_no)
    return log_levels_key_no, log_levels_key_name

def get_log_level_name(level_no):
    log_levels_key_no, _ = get_log_levels()
    return log_levels_key_no[level_no]

def get_log_level_no(level_name):
    _, log_levels_key_name = get_log_levels()
    return log_levels_key_name[level_name]

def current_log_level():
    """
    This function returns True if the current logging level is under
    'level' value
    """
    level_no = rh.logger._core.min_level
    level_name = get_log_level_name(level_no)

    return level_no, level_name

def is_being_logged(level_name='DEBUG'):
    current_log_level_no, _ = current_log_level()
    return current_log_level_no <= get_log_level_no(level_name)

def rename_if_exist(file_name, tail='.bak'):
    if os.path.isfile(file_name):
        rh.logger.warning("This file name already exists. Adding .bak")
        new_file_name = file_name + tail
        os.rename(file_name, new_file_name)


"""
MXNet + GluoncV
"""

def get_yolo_models():
    models = list(gcv.model_zoo.get_model_list())
    yolo_models = [models[i] for i in [176, 177, 179, 180, 182, 183]]
    return yolo_models

def get_rcnn_models():
    models = list(gcv.model_zoo.get_model_list())
    rcnn_models = [models[i] for i in [84, 86, 87, 88, 89, 91, 92, 93, 94, 95, 97]]
    return rcnn_models

def nn_out2df(class_ids, scores, bounding_boxs):
    # to DataFrame

    df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                columns=['class_ids'])
    df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                             columns=['scores'])
    df_bounding_boxs = pd.DataFrame(
        bounding_boxs.asnumpy()[0].tolist(),
        columns=['xmin', 'ymin', 'xmax', 'ymax'])

    return [df_class_ids, df_scores, df_bounding_boxs]

def object_detection_with_gluoncv(img,
                                  model='yolo3_darknet53_coco',
                                  gpu=False):
    """ Using a pre-trained model for object detection using GluonCV

    Parameters
    ----------
    img: a preloaded image with HWC layout
    model: a string with the model to apply
    gpu: boolean indicating if gpu context must be used

    Returns
    -------
    nn_out: a list with three MXNet ndarrays [class_ids, scores, bounding_boxs]
    df_nn_out: a dataframe with the three MXNet ndarrays converted
               to dataframes
    """

    yolo_models = get_yolo_models()
    rcnn_models = get_rcnn_models()

    if model not in yolo_models + rcnn_models:
        raise Exception(f"Sorry, the model '{model}' is not allowed")

    #  Set context to cpu or gpu
    ctx_ = mx.context.gpu() if gpu else mx.context.cpu()

    # Load Pretrained Model from the CV model zoo
    net = gcv.model_zoo.get_model(model,
                                  pretrained=True,
                                  ctx=ctx_)

    # Transform the Image

    """Function that applies all of the necessary preprocessing steps for the
    yolo network

    Outputs:

    trnf_img    the transformed image that is ready to be given to the network.
    chw_img     a resized version of the image for plotting results
                - It’s in NCHW format instead of NHWC format
                - It’s an array of 32-bit floats instead of 8-bit integers
                - It’s normalized using the image net 1K statistics
                - It can be plotted because it’s in the CHW format that is
                  used by pipeline: plt.imshow(chw_image)

    Note about CHW/HCW layouts (https://github.com/Microsoft/CNTK/issues/276):

     It is essentially the same terminology that is used by cuDNN (see cuDNN API
     reference/manual). cuDNN is a very popular library which is supported by
     all popular DNN toolkits, not just CNTK, so we decided to use the same
     terminology to simplify migration between the toolkits. Note that cuDNN
     also uses N for a sample in a batch and D for the depth dimension used,
     for example, in 3D convolutions, so full description of the data layout
     may look like: NCHW

    H: height
    W: width
    C: channels (3 for color images, 1 for B&W images)

    CHW: RR...R, GG..G, BB..B
    HWC: RGB, RGB, ... RGB

    """
    short_edge_size = min(img.shape[0:2])

    if model in yolo_models:
        rh.logger.trace("yolo_model: {}", model)
        trnf_img, chw_img = gcv.data.transforms.presets.yolo.transform_test(mx.nd.array(img),
                                                                            short=short_edge_size)
    if model in rcnn_models:
        rh.logger.trace("rcnn_model: {}", model)
        trnf_img, chw_img = gcv.data.transforms.presets.rcnn.transform_test(mx.nd.array(img),
                                                                            short=short_edge_size)


    """ Make prediction
    It returns three MXNet ndarrays:
    1st array contains the object class indexes.
        shape : (1, 100, 1)
        1 image
        100 potential objects
        1 class index per object
    2nd array contains the object class probabilities.
        shape : (1, 100, 1)
        1 image
        100 potential objects
        1 object class probability (score)
    3rd array contains the object bounding box coordinates.
        shape : (1, 100, 4)
        1 image
        100 potential objects
        4 values for each object to define its bounding box:
            xmin, ymin, xmax, ymax

    net.classes is an array with coco classes
    -1 is a special value used to indicate there is no detected object
    """
    class_ids, scores, bounding_boxs = net(trnf_img)

    nn_out = [class_ids, scores, bounding_boxs]

    return chw_img, net.classes, nn_out


"""
Lab
"""

def bin2rgba(img):
    """
    TODO
    """

    img = cv2.cvtColor(img*255, cv2.COLOR_GRAY2RGB)
    color_mask = np.random.random((1, 3)).tolist()[0]

    my_mask = cv2.compare(img,245,cv2.CMP_GT)
    img[my_mask > 0] = 255

    for i in range(3):
        img[:,:,i] = color_mask[i]*255
    plt.imshow(img, interpolation='nearest')
    plt.show()


