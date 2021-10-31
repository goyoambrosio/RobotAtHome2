#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/07/27"
__license__ = "MIT"

# import sys
# import datetime as dt
import sqlite3
import os
import numpy as np
import pandas as pd
# from pandas import read_sql_query
from robotathome import logger

__all__ = ['RobotAtHome']

class RobotAtHome():
    """RobotAtHome class with methods for Robot@Home dataset v2.x.y

    The RobotAtHome class encapsulates methods to access the RobotAtHome
    database. <https://doi.org/10.5281/zenodo.4530453>

    Attributes:
        rh_path (str, optional):
            root path for robotathome database, usually rh.db
        wspc_path (str, optional):
            workspace path where temporary files are stored
        db_filename (str, optional):
            default database name
        rgbd_path (str, optional):
           path that completes rh_path, where rgbd files are stored
        scene_path (str, optional):
           path that completes rh_path, where scene files are stored
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
        logger.debug("db_full_path: {}", db_full_path)

        try:
            self.__con = sqlite3.connect(db_full_path)
            logger.info("Connection is established: {}", self.__db_filename)
        except NameError:
            logger.error("Error while trying to open database: {}", NameError)

    def __close_dataset(self):
        """
        This function closes the connection with the database
        """
        self.__con.close()
        logger.info("The connection with the database has been successfully closed")

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
        logger.trace("The view rh_temp_lblrgbd has been created")

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
        # logger.debug(rows)
        # for row in rows:
        #     print(row)
        # logger.debug(rows2list(rows))

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

    def query(self, sql, df=True):
        """Execute a sqlquery over robotathome database

        Parameters
        ----------
        sql: can be a string with a sql query or a file name that contains the
             sql query
        df:  boolean indicating if result is returned as a DataFrame (True) or
             as a sqlite row list (False)

        Returns
        -------
        ans: a DataFrame or a sqlite row list

        """


        if os.path.isfile(sql):
            script = open(sql, 'r')
            query = script.read()
        else:
            query = sql

        if df:
            ans = pd.read_sql_query(query, self.__con)
        else:
            cur = self.__con.cursor()
            cur.executescript(query)
            ans = cur.fetchall()

        if os.path.isfile(sql):
            script.close()

        return ans

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

    def get_locators(self):
        """ Return a dataframe table with main indexes values (id and name),
        i.e., home_session, home, room and home_subsession
        """

        sql_str = """
        select
            home_session_id, rh_home_sessions.name as home_session_name,
            rh_raw.home_id, rh_homes.name as home_name,
            rh_raw.room_id, rh_rooms.name as room_name,
            rh_raw.home_subsession_id
        from rh_raw
        inner join rh_home_sessions on home_session_id = rh_home_sessions.id
        inner join rh_homes on rh_raw.home_id = rh_homes.id
        inner join rh_rooms on rh_raw.room_id = rh_rooms.id
        group by
            home_session_id,
            rh_raw.home_id,
            rh_raw.room_id,
            rh_raw.home_subsession_id

        order by
            rh_raw.home_session_id
        """

        df_rows = pd.read_sql_query(sql_str, self.__con)

        return df_rows

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
        #
        # parms = (home_session_name,
        #          home_subsession,
        #          room_name,
        #          sensor_name)
        # cur.execute(sql_str, parms)
        # cur.execute(sql_str)
        # rows = cur.fetchall()

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
        logger.debug(sql_str)

        df_rows = pd.read_sql_query(sql_str, self.__con)

        return df_rows

    def get_labels_from_lblrgbd(self, so_id):
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
        belong to rh_lblrgbd (labelled rgbd)
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

        logger.debug("mask height: {}", len(mask))
        logger.debug("mask width : {}", len(mask[0]))

        mask = np.array(mask)
        mask = np.rot90(mask)

        return mask

    def get_mask_from_lblrgbd(self, so_id):
        """
        This function 

        Parameters
        ----------

        Returns
        -------

        """
        # Get a cursor to execute SQLite statements
        # cur = self.__con.cursor()

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
        logger.debug("df_rows.shape: {}", df_rows.shape)
        # print(df_rows)
        # print(df_rows.loc[0,"pth"])
        # print(df_rows.loc[0,"f3"])
        label_path_file_name = os.path.join(self.__rh_path,
                                            self.__rgbd_path,
                                            df_rows.loc[0, "pth"],
                                            df_rows.loc[0, "f3"])

        logger.debug("label_path_file_name: {}", label_path_file_name)
        mask = self.__get_mask(label_path_file_name)

        return mask

    def get_label_mask(self, mask, labels):
        """
        Returns a binary 2D array (pixels being 1s and 0s)
        """
        masks = []
        for label in labels:
            arr = mask & (2**(label))
            np.clip(arr, 0, 1, out=arr)
            arr = np.uint8(arr[:,2:-2])
            masks.append(arr)
        return masks


    """
    Lab
    """

    def create_table_linking_observations_and_lblrgbd(self):
        """
        This function 

        Parameters
        ----------

        Returns
        -------

        """
        # Get a cursor to execute SQLite statements
        # cur = self.__con.cursor()

        sql_str_lblrgbd = (
            f'''
            select id, sensor_id
            from rh_lblrgbd
            order by id
            limit 860
            '''
        )

        sql_str_observations = (
            f'''
            select id, sensor_id
            from rh_observations
            order by id
            -- limit 20
            '''
        )

        df_rows_lblrgbd = pd.read_sql_query(sql_str_lblrgbd, self.__con)
        df_rows_observations = pd.read_sql_query(sql_str_observations, self.__con)

        # for row_lblrgbd in df_rows_lblrgbd.itertuples(index=False):
        #     print(row_lblrgbd)
        #     print(row_observation)

        i_obs = 0
        for i_lbl in range(df_rows_lblrgbd.shape[0]):
            if df_rows_lblrgbd['sensor_id'][i_lbl] == df_rows_observations['sensor_id'][i_obs]:
                print(df_rows_lblrgbd['id'][i_lbl], df_rows_observations['id'][i_obs])
                i_obs += 1

    def get_objects_from_sensor_observations(self, so_id):
        """TODO """
        pass

