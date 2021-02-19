#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/12"
__license__ = "MIT"

import sys
import time
import re
import datetime
import sqlite3
import os
import cv2
import pandas as pd
from mxnet import image
from gluoncv import model_zoo, data, utils
from matplotlib import pyplot as plt
import robotathome as rh
# import fire


def time_win2unixepoch(time_stamp):
    ''' Doctring '''
    seconds = time_stamp / 10000000
    epoch = seconds - 11644473600
    datetime_ = datetime.datetime(2000, 1, 1, 0, 0, 0)
    return datetime_.fromtimestamp(epoch)


def time_unixepoch2win(date):
    ''' Doctring '''
    match = re.compile(r'^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)$').match(date)
    if match:
        datetime_ = datetime.datetime(*map(int, match.groups()))
        windows_timestamp = (time.mktime(datetime_.timetuple()) + 11644473600) * 10000000
    else:
        print("Invalid date format specified: " + date)
        print("Specify a date and time string in the format: \"yyyy-MM-ddTHH:mm:ss\"")
        windows_timestamp = 0
    return windows_timestamp


def tup2list(tup):
    ''' Convert list of tuples into list '''
    return list(sum(tup, ()))


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
        ''' Return a list column names '''

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        # Build the query
        sql_str = ("select " + column_name + " from " + table_name + " group by " + column_name + ";")
        cur.execute(sql_str)
        return tup2list(cur.fetchall())

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
        sql_str = (
            '''
            select id, t, pth, f1, f2, f3
            from
            ''' +
            sensor_observation_table +
            '''
            where
                hs_name = ? and
                hss_id = ? and
                r_name = ? and
                s_name = ?
            order by t
            '''
        )

        parms = (home_session_name,
                 home_subsession,
                 room_name,
                 sensor_name)
        cur.execute(sql_str, parms)
        rows = cur.fetchall()

        return rows

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
        seconds = (rows[-1][1] - rows[0][1]) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows[0][2]
        file_name = rows[0][4]
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

        for row in rows:
            image_path = row[2]
            file_name = row[4]
            image_path_file_name = os.path.join(self.__rh_path,
                                                self.__rgbd_path,
                                                image_path,
                                                file_name)
            img = cv2.imread(image_path_file_name, cv2.IMREAD_COLOR)
            # cv2.imshow('img', img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            out.write(img)

        out.release()

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
        seconds = (rows_rgbd_1[-1][1] - rows_rgbd_1[0][1]) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows_rgbd_1[0][2]
        file_name = rows_rgbd_1[0][4]
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

        for i, _ in enumerate(rows_rgbd_1):
            image_rgbd_1_path = rows_rgbd_1[i][2]
            file_rgbd_1_name = rows_rgbd_1[i][4]
            image_rgbd_1_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_1_path,
                                                       file_rgbd_1_name)

            image_rgbd_2_path = rows_rgbd_2[i][2]
            file_rgbd_2_name = rows_rgbd_2[i][4]
            image_rgbd_2_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_2_path,
                                                       file_rgbd_2_name)

            image_rgbd_3_path = rows_rgbd_3[i][2]
            file_rgbd_3_name = rows_rgbd_3[i][4]
            image_rgbd_3_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_3_path,
                                                       file_rgbd_3_name)

            image_rgbd_4_path = rows_rgbd_4[i][2]
            file_rgbd_4_name = rows_rgbd_4[i][4]
            image_rgbd_4_path_file_name = os.path.join(self.__rh_path,
                                                       self.__rgbd_path,
                                                       image_rgbd_4_path,
                                                       file_rgbd_4_name)


            img_rgbd_1 = cv2.imread(image_rgbd_1_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_2 = cv2.imread(image_rgbd_2_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_3 = cv2.imread(image_rgbd_3_path_file_name, cv2.IMREAD_COLOR)
            img_rgbd_4 = cv2.imread(image_rgbd_4_path_file_name, cv2.IMREAD_COLOR)

            img = cv2.hconcat([img_rgbd_3, img_rgbd_4, img_rgbd_1, img_rgbd_2])

            # cv2.imshow('img', img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

            out.write(img)
        out.release()
        # cv2.destroyAllWindows()
        # return [rows_rgbd_1, rows_rgbd_2, rows_rgbd_3, rows_rgbd_4]
        return video_file_name

    def process_with_yolo(self,
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
        seconds = (rows[-1][1] - rows[0][1]) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows[0][2]
        file_name = rows[0][4]
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
        net = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)

        nn_out = []
        i = 0
        for row in rows:
            image_path = row[2]
            file_name = row[4]
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

            x, img = data.transforms.presets.yolo.load_test(image_path_file_name,
                                                            short=short_edge_size)
            # rh.logger.debug('Shape of pre-processed image: {}', x.shape)
            class_ids, scores, bounding_boxs = net(x)
            nn_out.append([class_ids, scores, bounding_boxs])
            utils.viz.cv_plot_bbox(img,
                                   bounding_boxs[0],
                                   scores[0],
                                   class_ids[0],
                                   class_names=net.classes,
                                   thresh=0.2,
                                   linewidth=1)

            out.write(img)

        out.release()

        return pd.DataFrame(nn_out), video_file_name

    def process_with_rcnn(self,
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
        seconds = (rows[-1][1] - rows[0][1]) / 10**7
        frames_per_second = num_of_frames / seconds
        rh.logger.debug("frames per second: {:.2f}", frames_per_second)

        # Get frame size
        image_path = rows[0][2]
        file_name = rows[0][4]
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
        net = model_zoo.get_model('yolo3_darknet53_coco', pretrained=True)

        nn_out = []
        i = 0
        for row in rows:
            image_path = row[2]
            file_name = row[4]
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
            nn_out.append([class_ids, scores, bounding_boxs])
            utils.viz.cv_plot_bbox(img,
                                   bounding_boxs[0],
                                   scores[0],
                                   class_ids[0],
                                   class_names=net.classes,
                                   thresh=0.2,
                                   linewidth=1)
            out.write(img)

        out.release()

        return pd.DataFrame(nn_out), video_file_name


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
