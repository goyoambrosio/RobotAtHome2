#!/usr/bin/env python
# -*- coding: utf-8; buffer-read-only: t -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2023, Gregorio Ambrosio"
__date__ = "2023/02/20"
__license__ = "MIT"


import cv2
from robotathome import logger


__all__ = ['filter_sensor_observations',
           'get_frames_per_second',
           'get_RGBD_image',
           'RGBD_images',
           'composed_RGBD_images']


def filter_sensor_observations(rh_dataset, df,
                               home_session_name='alma-s1',
                               home_subsession=0,
                               room_name='alma_masterroom1',
                               sensor_list=['RGBD_3',
                                            'RGBD_4',
                                            'RGBD_1',
                                            'RGBD_2']
                               ):
    """Return a dictionary with an item per sensor.

    This function applies a filter to the dataframe to select data
    for a home session and home subsession, a room name, and a list
    of sensor names.

    Args:
        rh_dataset: a robotathome object to get the id associated to a name
        df: a Pandas dataframe with the data resulting from the
            execution of the RoboAtHome:get_sensor_observations method.
        home_session_name: a string with the home session name
        home_subsession: the subsession number (0 or 1)
        room_name: a string with the room name
        sensor_list: a list made up of the names of the sensors

    Returns:
        df_dict: a dictionary with a item per sensor. Keys are the sensor
        names, and values are the filtered dataframe for that sensor.
    """
    # We need to get some ids from names because
    home_session_id = rh_dataset.name2id(home_session_name, 'hs')
    room_id = rh_dataset.name2id(room_name, 'r')

    qstr1 = f'home_session_id=={home_session_id}'
    qstr2 = f'home_subsession_id=={home_subsession}'
    qstr3 = f'room_id=={room_id}'

    df_dict = {}

    # Apply filter a get the corresponding subset
    for sensor_name in sensor_list:
        sensor_id = rh_dataset.name2id(sensor_name, 's')
        qstr4 = f'sensor_id=={sensor_id}'
        df_query_str = qstr1 + ' & ' + qstr2 + ' & ' + qstr3 + ' & ' + qstr4
        df_dict[sensor_name] = df.query(df_query_str)
    return df_dict


def get_frames_per_second(df):
    """Compute frames per second for a sensor observations dataframe.

    Args:
        df: a Pandas dataframe with the data resulting from the
            execution of the RoboAtHome:get_sensor_observations method.

    Returns:
        frames_per_second: the result of calculating the time between the
        first frame and the last frame divided by the number of frames
    """
    # Computing frames per second
    num_of_frames = len(df.index)
    seconds = (df.iloc[-1]['timestamp'] - df.iloc[0]['timestamp']) / 10**7
    frames_per_second = num_of_frames / seconds
    logger.debug("frames per second: {:.2f}", frames_per_second)
    return frames_per_second


def get_RGBD_image(rh_dataset, row):
    """Return a tuple composed of RGB & D images."""
    [rgb_f, d_f] = rh_dataset.get_RGBD_files(row['id'])
    RGBD_image = (cv2.imread(rgb_f, cv2.IMREAD_COLOR),
                  cv2.imread(d_f,   cv2.IMREAD_COLOR))
    return RGBD_image


def RGBD_images(rh_dataset, df):
    """ Return a generator function of images."""
    for _, row in df.iterrows():
        img = get_RGBD_image(rh_dataset, row)
        yield img


def composed_RGBD_images(rh_dataset, df_dict):
    """ Return a generator function of composed images.

    Returns:
        A dictionary whose keys are sensor names (sensor_list) and values are
        tuples of RGB image list and D image list of the corresponding sensor.

    """
    # Yield over df_dict, i.e. frame by frame
    df_list = list(df_dict.values())  # Get a list of dataframes
    sensor_list = list(df_dict.keys())
    df_lengths = [len(df) for df in df_list]  # Get a list of df's lengths
    number_of_rows = min(df_lengths)  # Select the minumun length

    # For each row we will make a composed image
    for row_index in range(number_of_rows):
        # For each sensor we will append an image to img_list
        RGB_image_list = []  # initialization of img_list
        D_image_list = []
        for df in df_list:
            row = df.iloc[row_index]
            RGBD_image = get_RGBD_image(rh_dataset, row)
            RGB_image_list.append(RGBD_image[0])
            D_image_list.append(RGBD_image[1])
        RGB_image_dict = dict(zip(sensor_list, RGB_image_list))
        D_image_dict = dict(zip(sensor_list, D_image_list))
        yield (RGB_image_dict, D_image_dict)