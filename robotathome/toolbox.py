#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/22"
__license__ = "MIT"

import sys
import time
import re
import datetime as dt
import sqlite3
import os
import cv2
import numpy as np
import pandas as pd
from mxnet import image
from mxnet import context
from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
import robotathome as rh
# import fire


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


class RobotAtHome():
    """
    RobotAtHome class with methods to manage the Robot@Home dataset v2.x.y
    """

    def __init__(self,
                 rh_path='.',
                 wspc_path='.',
                 db_filename='rh.db',
                 rgbd_path='files/rgbd',
                 scene_path='files/scene'):
        """ RobotAtHome constructor method """
        self.__rh_path = rh_path
        self.__wspc_path = wspc_path
        self.__db_filename = db_filename
        self.__rgbd_path = rgbd_path
        self.__scene_path = scene_path
        self.__con = None
        self.__rgbd_views = []

        # Initialization functions
        self.__open_dataset()
        self.__create_temp_views()

    def __del__(self):
        """ Robot@Home destructor method"""

    def __open_dataset(self):

        """
        This function makes the connection with the database and calls the
        initialization functions, e.g. create temporal views
        """

        db_full_path = os.path.join(self.__rh_path, self.__db_filename)
        rh.logger.debug("db_full_path: {}", db_full_path)

        try:
            self.__con = sqlite3.connect(db_full_path)
            rh.logger.info("Connection is established: {}", self.__db_filename)
        except NameError:
            rh.logger.error("Error while trying to open database: {}", NameError)

    def __close_dataset(self):
        """
        This function closes the connection with the database
        """
        self.__con.close()
        rh.logger.info("The connection with the database has been successfully closed")

    def __create_temp_views(self):
        """
        This function creates temporary views to work on the class environment
        """

        sql_str = '''
        begin transaction;
        drop view if exists rh_temp_lblrgbd;
        create temp view rh_temp_lblrgbd as
        select
            rh_lblrgbd.id,
            rh_lblrgbd.home_session_id as hs_id,
            rh_home_sessions.name as hs_name,
            rh_lblrgbd.home_subsession_id as hss_id,
            rh_lblrgbd.home_id as h_id,
            rh_homes.name as h_name,
            rh_lblrgbd.room_id as r_id,
            rh_rooms.name as r_name,
            rh_lblrgbd.sensor_id as s_id,
            rh_sensors.name as s_name,
            rh_lblrgbd.time_stamp as t,
            rh_lblrgbd.sensor_pose_x as s_px,
            rh_lblrgbd.sensor_pose_y as s_py,
            rh_lblrgbd.sensor_pose_z as s_pz,
            rh_lblrgbd.sensor_pose_yaw as s_pya,
            rh_lblrgbd.sensor_pose_pitch as s_ppi,
            rh_lblrgbd.sensor_pose_roll as s_pro,
            rh2_old2new_rgbd_files.new_file_1 as f1,
            rh2_old2new_rgbd_files.new_file_2 as f2,
            rh2_old2new_rgbd_files.new_file_3 as f3,
            rh2_old2new_rgbd_files.new_path as pth
        from rh_lblrgbd
        inner join rh_home_sessions on home_session_id = rh_home_sessions.id
        inner join rh_homes on rh_lblrgbd.home_id = rh_homes.id
        inner join rh_rooms on rh_lblrgbd.room_id = rh_rooms.id
        inner join rh_sensors on rh_lblrgbd.sensor_id = rh_sensors.id
        inner join rh2_old2new_rgbd_files on rh2_old2new_rgbd_files.id = rh_lblrgbd.id;
        commit;
        '''

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()
        cur.executescript(sql_str)

        self.__rgbd_views.append("rh_temp_lblrgbd")
        rh.logger.trace("The view rh_temp_lblrgbd has been created")

    def get_con(self):
        """
        This function returns the sql connection variable
        """
        return self.__con

    def select_column(self, column_name, table_name):
        '''
        Returns a dataframe with grouped column values
        (without repetition)
        '''

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        # Build the query
        # sql_str = ("select " + column_name + " from " + table_name + " group by " + column_name + ";")
        # rows = cur.execute(sql_str)
        # rh.logger.debug(rows)
        # for row in rows:
        #     print(row)
        # rh.logger.debug(rows2list(rows))

        sql_str = (f"select {column_name}  from {table_name} group by {column_name};")
        df_rows = pd.read_sql_query(sql_str, self.__con)
        return df_rows

    def __get_temp_sql_object_names(self):
        ''' Return a list with temporary/internal created views'''
        return self.select_column('tbl_name', 'sqlite_temp_master')

    def get_rh2_rgbd_views(self):
        """
        Return a list with RGB-D views
        """
        # There is only one view for now
        return self.__rgbd_views

    def get_home_session_names(self):
        """
        Return a list with home session names
        """
        return self.select_column('name', 'rh_home_sessions')

    def get_home_names(self):
        """
        Return a list with home names '''
        """
        return self.select_column('name', 'rh_homes')

    def get_room_names(self):
        """
        Return a list with room names
        """
        return self.select_column('name', 'rh_rooms')

    def get_room_type_names(self):
        """
        Return a list with room type names
        """
        return self.select_column('name', 'rh_room_types')

    def get_sensor_names(self):
        """
        Return a list with sensor names
        """
        return self.select_column('name', 'rh_sensors')

    def get_sensor_type_names(self):
        """
        Return a list with sensor type names
        """
        return self.select_column('name', 'rh_sensor_types')

    def get_object_type_names(self):
        """
        Return a list with room type names
        """
        return self.select_column('name', 'rh_object_types')

    def get_sensor_observation_files(self,
                                     source='lblrgbd',
                                     home_session_name='alma-s1',
                                     home_subsession=0,
                                     room_name='alma_masterroom1',
                                     sensor_name='RGBD_1'
                                     ):

        """
        This functions queries the database to extract sensor observation
        files filtered by home_session_name, home_subsession, room_name, and
        sensor_name.
        """

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        switcher = {
            # rh_temp_lblrgbd created in _create_temp_views at the begining
            "lblrgbd": "rh_temp_lblrgbd",
        }
        sensor_observation_table = switcher.get(source, lambda: "Invalid argument")

        # Build the query
        # sql_str = (
        #     '''
        #     select id, t, pth, f1, f2, f3
        #     from
        #     ''' +
        #     sensor_observation_table +
        #     '''
        #     where
        #         hs_name = ? and
        #         hss_id = ? and
        #         r_name = ? and
        #         s_name = ?
        #     order by t
        #     '''
        # )

        # parms = (home_session_name,
        #          home_subsession,
        #          room_name,
        #          sensor_name)
        # cur.execute(sql_str, parms)

        sql_str = (
            f'''
            select id, t, pth, f1, f2, f3
            from {sensor_observation_table}
            where
                hs_name = '{home_session_name}' and
                hss_id = {home_subsession} and
                r_name = '{room_name}' and
                s_name = '{sensor_name}'
            order by t
            '''
        )
        rh.logger.debug(sql_str)

        # cur.execute(sql_str)
        # rows = cur.fetchall()
        df_rows = pd.read_sql_query(sql_str, self.__con)

        return df_rows

    def get_video_from_rgbd(self,
                            source='lblrgbd',
                            home_session_name='alma-s1',
                            home_subsession=0,
                            room_name='alma_masterroom1',
                            sensor_name='RGBD_1',
                            video_file_name=None
                            ):

        """
        This functions ...
        """

        rows = self.get_sensor_observation_files(source,
                                                 home_session_name,
                                                 home_subsession,
                                                 room_name,
                                                 sensor_name)

        # Computing frames per second
        num_of_frames = len(rows)
        seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows.iloc[0]['pth']
        file_name = rows.iloc[0]['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
        img_h, img_w, _ = img.shape

        # Opening video file
        if video_file_name is None:
            video_file_name = ''.join(
                [
                    home_session_name,
                    '_', str(home_subsession),
                    '_', room_name,
                    '_', sensor_name,
                    dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                    '.avi'
                ]
            )
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                            video_file_name)
                                               )
        out = cv2.VideoWriter(video_path_file_name,
                              fourcc,
                              frames_per_second,
                              (img_w, img_h))

        for _, row in rows.iterrows():
            image_path = row['pth']
            file_name = row['f2']
            image_path_file_name = os.path.join(self.__rh_path,
                                                self.__rgbd_path,
                                                image_path,
                                                file_name)
            img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)

            if rh.is_being_logged():
                cv2.imshow('Debug mode (press q to exit)', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            out.write(img)

        out.release()

        if rh.is_being_logged():
            cv2.destroyAllWindows()

        return video_file_name

    def get_composed_video_from_lblrgbd(self,
                                        home_session_name='alma-s1',
                                        home_subsession=0,
                                        room_name='alma_masterroom1',
                                        video_file_name=None
                                        ):

        ''' Docstring '''

        rows_rgbd_1 = self.get_sensor_observation_files('lblrgbd',
                                                        home_session_name,
                                                        home_subsession,
                                                        room_name,
                                                        'RGBD_1')

        rows_rgbd_2 = self.get_sensor_observation_files('lblrgbd',
                                                        home_session_name,
                                                        home_subsession,
                                                        room_name,
                                                        'RGBD_2')

        rows_rgbd_3 = self.get_sensor_observation_files('lblrgbd',
                                                        home_session_name,
                                                        home_subsession,
                                                        room_name,
                                                        'RGBD_3')

        rows_rgbd_4 = self.get_sensor_observation_files('lblrgbd',
                                                        home_session_name,
                                                        home_subsession,
                                                        room_name,
                                                        'RGBD_4')

        # Computing frames per second
        num_of_frames = len(rows_rgbd_1)
        seconds = (rows_rgbd_1.iloc[-1]['t'] - rows_rgbd_1.iloc[0]['t']) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows_rgbd_1.iloc[0]['pth']
        file_name = rows_rgbd_1.iloc[0]['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
        img_h, img_w, _ = img.shape

        # Opening video file
        if video_file_name is None:
            video_file_name = ''.join(
                [
                    home_session_name,
                    '_', str(home_subsession),
                    '_', room_name,
                    '_RGBD_3412',
                    dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                    '.avi'
                ]
            )

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                            video_file_name))
        out = cv2.VideoWriter(video_path_file_name,
                              fourcc,
                              frames_per_second,
                              (4 * img_w, img_h))

        for i in range(len(rows_rgbd_1)):
            image_rgbd_1_path = rows_rgbd_1.iloc[i, 2]
            file_rgbd_1_name = rows_rgbd_1.iloc[i, 4]
            image_rgbd_1_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_1_path,
                                                       file_rgbd_1_name)

            image_rgbd_2_path = rows_rgbd_2.iloc[i, 2]
            file_rgbd_2_name = rows_rgbd_2.iloc[i, 4]
            image_rgbd_2_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_2_path,
                                                       file_rgbd_2_name)

            image_rgbd_3_path = rows_rgbd_3.iloc[i, 2]
            file_rgbd_3_name = rows_rgbd_3.iloc[i, 4]
            image_rgbd_3_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_3_path,
                                                       file_rgbd_3_name)

            image_rgbd_4_path = rows_rgbd_4.iloc[i, 2]
            file_rgbd_4_name = rows_rgbd_4.iloc[i, 4]
            image_rgbd_4_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_4_path,
                                                       file_rgbd_4_name)


            img_rgbd_1 = cv2.imread(image_rgbd_1_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_2 = cv2.imread(image_rgbd_2_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_3 = cv2.imread(image_rgbd_3_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_4 = cv2.imread(image_rgbd_4_path_file_name, cv2.IMREAD_COLOR)

            img = cv2.hconcat([img_rgbd_3, img_rgbd_4, img_rgbd_1, img_rgbd_2])

            if rh.is_being_logged():
                cv2.imshow('Debug mode (press q to exit)', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            out.write(img)
        out.release()

        if rh.is_being_logged():
            cv2.destroyAllWindows()

        return video_file_name

    def get_labels_from_sensor_observation(self, so_id):
        """
        This function return labels rows for the observations referenced by
        sensor_observation_id

        SQL query

        select * from rh_lblrgbd_labels
            where sensor_observation_id = so_id

        Parameters
        ----------
        so_id : int
            The primary key value to identify a row in the table
            rh_lbl_rgbd_labels.

        Returns
        -------
        A dataframe with the query result. An empty dataframe is returned when
        no rows are available, i.e., when the sensor observation does not
        belong to rh_lblrgbd (lebelled rgbd)
        """

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        # # Build the query
        # sql_str = (
        #     '''
        #     select * from rh_lblrgbd_labels
        #     where sensor_observation_id = ?
        #     '''
        # )

        # parms = (so_id,)
        # cur.execute(sql_str, parms)
        # rows = cur.fetchall()

        sql_str = (
            '''
            select * from rh_lblrgbd_labels
            where sensor_observation_id = {}
            '''.format(so_id)
        )

        df_rows = pd.read_sql_query(sql_str, self.__con)

        # print(df.shape)
        # rows = df.to_records()
        # for row in rows:
        #     print(row)

        return df_rows

    def __get_mask(self, label_path_file_name):
        mask = []
        with open(label_path_file_name, "r") as file_handler:
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

        rh.logger.debug("mask height: {}", len(mask))
        rh.logger.debug("mask width : {}", len(mask[0]))

        return mask

    def get_image_mask_from_label(self, mask, label_id):
        arr = np.array(mask)
        arr = np.rot90(arr)
        arr = arr & (2**(label_id))
        np.clip(arr, 0, 1, out=arr)
        arr = np.uint8(arr)
        # arr = arr * 255
        return arr

    def get_mask_from_sensor_observation(self, so_id):
        """
        This function 

        Parameters
        ----------

        Returns
        -------

        """
        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        # sql_str = (
        #     '''
        #     select pth, f3
        #     from rh_temp_lblrgbd
        #     where id = {}
        #     '''.format(so_id)
        # )

        sql_str = (
            f'''
            select pth, f3
            from rh_temp_lblrgbd
            where id = {so_id}
            '''
        )

        df_rows = pd.read_sql_query(sql_str, self.__con)
        rh.logger.debug("df_rows.shape: {}", df_rows.shape)        
        # print(df_rows)
        # print(df_rows.loc[0,"pth"])
        # print(df_rows.loc[0,"f3"])
        label_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            df_rows.loc[0, "pth"],
                                            df_rows.loc[0, "f3"])

        rh.logger.debug("label_path_file_name: {}", label_path_file_name)
        mask = self.__get_mask(label_path_file_name)

        return mask

    def process_with_yolo(self,
                          source='lblrgbd',
                          home_session_name='alma-s1',
                          home_subsession=0,
                          room_name='alma_masterroom1',
                          sensor_name='RGBD_1',
                          video_file_name=None,
                          gpu=False
                          ):

        """
        This functions ...
        """

        rows = self.get_sensor_observation_files(source,
                                                 home_session_name,
                                                 home_subsession,
                                                 room_name,
                                                 sensor_name)

        # Computing frames per second
        num_of_frames = len(rows)
        seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows.iloc[0]['pth']
        file_name = rows.iloc[0]['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
        img_h, img_w, _ = img.shape

        # Opening video file
        if video_file_name is None:
            video_file_name = ''.join(
                [
                    home_session_name,
                    '_', str(home_subsession),
                    '_', room_name,
                    '_', sensor_name,
                    '_by_YOLO',
                    dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                    '.avi'
                ]
            )
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                            video_file_name)
                                               )
        rh.rename_if_exist(video_path_file_name)

        out = cv2.VideoWriter(video_path_file_name,
                              fourcc,
                              frames_per_second,
                              (img_w, img_h))



        ##############################################
        #                     NN
        ##############################################


        #  get NN model
        ctx_ = context.gpu() if gpu else context.cpu()
        net = model_zoo.get_model('yolo3_darknet53_coco',
                                  pretrained=True,
                                  ctx=ctx_)

        nn_out = []
        i = 0
        for _, row in rows.iterrows():
            image_path = row['pth']
            file_name = row['f2']
            image_path_file_name = os.path.join(self.__rh_path,
                                                self.__rgbd_path,
                                                image_path,
                                                file_name)
            i += 1
            if rh.is_being_logged('INFO'):
                sys.stdout.write("\rProcessing frame %i of %i" % (i, len(rows)))
                sys.stdout.flush()

            # core
            try:
                img = image.imread(image_path_file_name)
            except:
                print('%s is not a valid raster image' % image_path_file_name)

            # long_edge_size = img.shape[0]
            short_edge_size = img.shape[1]

            x, img = data.transforms.presets.yolo.load_test(image_path_file_name,
                                                            short=short_edge_size)
            # rh.logger.debug('Shape of pre-processed image: {}', x.shape)
            class_ids, scores, bounding_boxs = net(x)

            # to DataFrame
            df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                        columns=['class_ids'])
            df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                                     columns=['scores'])
            df_bounding_boxs = pd.DataFrame(
                bounding_boxs.asnumpy()[0].tolist(),
                columns=['xmin', 'ymin', 'xmax', 'ymax'])

            nn_out.append([df_class_ids,
                           df_scores,
                           df_bounding_boxs])

            utils.viz.cv_plot_bbox(img,
                                   bounding_boxs[0],
                                   scores[0],
                                   class_ids[0],
                                   class_names=net.classes,
                                   thresh=0.2,
                                   linewidth=1)
            if rh.is_being_logged():
                cv2.imshow('Debug mode (press q to exit)', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            out.write(img)

        out.release()

        if rh.is_being_logged():
            cv2.destroyAllWindows()

        df_nn_out = pd.DataFrame(nn_out, columns=['class_ids',
                                                  'scores',
                                                  'bounding_boxs'])
        return df_nn_out, video_file_name

    def process_with_rcnn(self,
                          source='lblrgbd',
                          home_session_name='alma-s1',
                          home_subsession=0,
                          room_name='alma_masterroom1',
                          sensor_name='RGBD_1',
                          video_file_name=None,
                          gpu=False
                          ):

        """
        This functions ...
        """

        rows = self.get_sensor_observation_files(source,
                                                 home_session_name,
                                                 home_subsession,
                                                 room_name,
                                                 sensor_name)

        # Computing frames per second
        num_of_frames = len(rows)
        seconds = (rows.iloc[-1]['t'] - rows.iloc[0]['t']) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows.iloc[0]['pth']
        file_name = rows.iloc[0]['f2']
        image_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            image_path,
                                            file_name)
        img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
        img_h, img_w, _ = img.shape

        # Opening video file
        if video_file_name is None:
            video_file_name = ''.join(
                [
                    home_session_name,
                    '_', str(home_subsession),
                    '_', room_name,
                    '_', sensor_name,
                    '_by_RCNN',
                    dt.datetime.now().strftime("_%Y%m%d%H%M%S"),
                    '.avi'
                ]
            )
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video_path_file_name = os.path.abspath(os.path.join(self.__wspc_path,
                                                            video_file_name)
                                               )
        out = cv2.VideoWriter(video_path_file_name,
                              fourcc,
                              frames_per_second,
                              (img_w, img_h))



        ##############################################
        #                     NN
        ##############################################


        #  get NN model
        # import mxnet as mx
        # ctx = mx.gpu() if gpu else mx.cpu()  # Set context
        # ctx = context.cpu()
        # ctx = context.cpu_pinned()
        # ctx = context.gpu(dev_id)
        ctx_ = context.gpu() if gpu else context.cpu()
        net = model_zoo.get_model('faster_rcnn_resnet50_v1b_coco',
                                  pretrained=True,
                                  ctx=ctx_) 
        nn_out = []
        i = 0
        for _, row in rows.iterrows():
            image_path = row['pth']
            file_name = row['f2']
            image_path_file_name = os.path.join(self.__rh_path,
                                                self.__rgbd_path,
                                                image_path,
                                                file_name)
            i += 1
            sys.stdout.write("\rProcessing frame %i of %i" % (i, len(rows)))
            sys.stdout.flush()

            # core
            try:
                img = image.imread(image_path_file_name)
            except:
                print('%s is not a valid raster image' % image_path_file_name)

            # long_edge_size = img.shape[0]
            short_edge_size = img.shape[1]

            x, img = data.transforms.presets.rcnn.load_test(image_path_file_name,
                                                            short=short_edge_size)
            # rh.logger.debug('Shape of pre-processed image: {}', x.shape)
            class_ids, scores, bounding_boxs = net(x)
            # to DataFrame
            df_class_ids = pd.DataFrame(class_ids.asnumpy()[0].tolist(),
                                        columns=['class_ids'])
            df_scores = pd.DataFrame(scores.asnumpy()[0].tolist(),
                                     columns=['scores'])
            df_bounding_boxs = pd.DataFrame(
                bounding_boxs.asnumpy()[0].tolist(),
                columns=['xmin', 'ymin', 'xmax', 'ymax'])

            nn_out.append([df_class_ids,
                           df_scores,
                           df_bounding_boxs])

            utils.viz.cv_plot_bbox(img,
                                   bounding_boxs[0],
                                   scores[0],
                                   class_ids[0],
                                   class_names=net.classes,
                                   thresh=0.2,
                                   linewidth=1)
            if rh.is_being_logged():
                cv2.imshow('Debug mode (press q to exit)', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            out.write(img)

        out.release()

        if rh.is_being_logged():
            cv2.destroyAllWindows()

        df_nn_out = pd.DataFrame(nn_out, columns=['class_ids',
                                                  'scores',
                                                  'bounding_boxs'])
        return df_nn_out, video_file_name


def main():

    """ Docstring """

    # fire.Fire()

    # try:
    #     fire.Fire(<function>)
    # except Exception as e:
    #     print("Oops! ", sys.exc_info()[0], " occurred.")
    #     print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    # rh.enable_logger(sink=sys.stderr, level="TRACE")
    rh.logger.trace("Running main() from toolbox.py")

    # print(rh.version.get_version_str())

    # main return
    return 0


if __name__ == "__main__":
    main()
