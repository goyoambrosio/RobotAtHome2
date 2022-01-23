#!/usr/bin/env python
# -*- coding: utf-8; buffer-read-only: t -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/07/27"
__license__ = "MIT"

import sqlite3
import os
import numpy as np
import pandas as pd
from robotathome.log import logger

__all__ = ['RobotAtHome']

# @logger.catch
class RobotAtHome():
    """RobotAtHome class with methods for Robot@Home2 dataset

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
                 rgbd_path='./files/rgbd',
                 scene_path='./files/scene',
                 wspc_path='.',
                 db_filename='rh.db'
                 ):
        """ RobotAtHome constructor method """
        self.__rh_path = os.path.expanduser(rh_path)
        self.__rgbd_path = os.path.expanduser(rgbd_path)
        self.__scene_path = os.path.expanduser(scene_path)
        self.__wspc_path = os.path.expanduser(wspc_path)
        self.__db_filename = db_filename
        self.__con = None
        self.__aliases = {}

        logger.debug('rh_path     : {}', self.__rh_path)
        logger.debug('rgbd_path   : {}', self.__rgbd_path)
        logger.debug('scene_path  : {}', self.__scene_path)
        logger.debug('wspc_path   : {}', self.__wspc_path)
        logger.debug('db_filename : {}', self.__db_filename)

        # Initialization functions
        try:
            self.__open_dataset()
        except Exception as e:
            logger.error("object cannot be instantiated")
            # return None
            raise e
        else:
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
            db_full_filename = 'file:'+db_full_path+'?mode=rw'
            logger.debug("db_full_filename: {}", db_full_filename)
            self.__con = sqlite3.connect(db_full_filename, uri=True)
            logger.success("Connection is established: {}", self.__db_filename)
        except sqlite3.Error as e:
            logger.error("Error while trying to open database: {}", e.args[0])
            # sys.exit() , quit() , exit() ,raise SystemExit
            # os._exit(1)
            raise

    def __close_dataset(self):
        """
        This function closes the connection with the database
        """
        self.__con.close()
        logger.info("The connection with the database has been successfully closed")

    def __get_temp_sql_object_names(self):
        ''' Return a list with temporary/internal created views'''
        return self.select_column('tbl_name', 'sqlite_temp_master')

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

    def query(self, sql, df=True):
        """Execute a sqlquery over robotathome database

        Parameters
        ----------
        sql: can be a string with a sql query or a file name that contains the
             sql query
        df:  boolean indicating if result is returned as a DataFrame (True) or
             as a sqlite row list (False).  This option (False) is mandatory if
             the query string has more than one sql command, i.e., it's a script

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


    """
    Framework
    """
    def get_homes(self):
        """
        Return a dataframe with home names
        """
        sql_str = ('select * from rh_homes;')
        return self.query(sql_str)

    def get_home_sessions(self):
        """
        Return a dataframe with home session names
        """
        sql_str = ('select * from rh_home_sessions;')
        return self.query(sql_str)
    def get_rooms(self):
        """
        Return a dataframe with room names
        """
        sql_str = ('select * from rh_rooms;')
        return self.query(sql_str)
    def get_room_types(self):
        """
        Return a dataframe with room type names
        """
        sql_str = ('select * from rh_room_types;')
        return self.query(sql_str)
    def get_sensors(self):
        """
        Return a dataframe with sensor names
        """
        sql_str = ('select * from rh_sensors;')
        return self.query(sql_str)
    def get_sensor_types(self):
        """
        Return a dataframe with sensor type names
        """
        sql_str = ('select * from rh_sensor_types;')
        return self.query(sql_str)
    def get_hometopo(self):
        """
        Return a dataframe with home topo relationships
        """
        sql_str = ('''
        select
            rh_homes.id as home_id,
            rh_homes.name as home_name,
	        rh_rooms1.id as room1_id,
	        rh_rooms1.name as room1_name,
	        rh_rooms2.id as room2_id,
	        rh_rooms2.name as room2_name
        from rh_hometopo
        inner join rh_homes on rh_hometopo.home_id = rh_homes.id
        inner join rh_rooms as rh_rooms1 on rh_rooms1.id = rh_hometopo.room1_id
        inner join rh_rooms as rh_rooms2 on rh_rooms2.id = rh_hometopo.room2_id
        '''
        )
        return self.query(sql_str)

    def get_locators(self):
        """ Return a dataframe with main indexes values (id and name),
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



    """
    Captured data
    """
    def get_sensor_observations(self, arg='full'):
        """ Docstring """

        def get_full_data():
            """ Docstring """
            sql_str = (
                f'''
                select
                    id, time_stamp as timestamp,
                    home_session_id, home_subsession_id, home_id, room_id,
                    sensor_id, name as sensor_name,
                    sensor_pose_x, sensor_pose_y, sensor_pose_z,
                    sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll
                from rh2_sensor_observations
                order by time_stamp
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_discarded_data():
            """ Docstring """
            sql_str = (
                f'''
                select
                    id, time_stamp as timestamp,
                    home_session_id, home_subsession_id, home_id, room_id,
                    sensor_id, name as sensor_name,
                    sensor_pose_x, sensor_pose_y, sensor_pose_z,
                    sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll
                from rh2_sensor_observations
                where id < 100000
                order by time_stamp
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_lblrgbd_data():
            """ Docstring """
            sql_str = (
                f'''
                select
                    id, time_stamp as timestamp,
                    home_session_id, home_subsession_id, home_id, room_id,
                    sensor_id, name as sensor_name,
                    sensor_pose_x, sensor_pose_y, sensor_pose_z,
                    sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll
                from rh2_sensor_observations
                where id >= 100000 and id < 200000 
                order by time_stamp
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_lsrscan_data():
            """ Docstring """
            sql_str = (
                f'''
                select
                    id, time_stamp as timestamp,
                    home_session_id, home_subsession_id, home_id, room_id,
                    sensor_id, name as sensor_name,
                    sensor_pose_x, sensor_pose_y, sensor_pose_z,
                    sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll
                from rh2_sensor_observations
                where id >= 200000
                order by time_stamp
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_rgbd_lsr_data():
            """ Docstring """
            sql_str = (
                f'''
                select
                    id, time_stamp as timestamp,
                    home_session_id, home_subsession_id, home_id, room_id,
                    sensor_id, name as sensor_name,
                    sensor_pose_x, sensor_pose_y, sensor_pose_z,
                    sensor_pose_yaw, sensor_pose_pitch, sensor_pose_roll
                from rh2_sensor_observations
                where id >= 100000 and id < 300000
                order by time_stamp
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)


        switcher = {
            "full"      : get_full_data,
            "discarded" : get_discarded_data,
            "lblrgbd"   : get_lblrgbd_data,
            "lsrscan"   : get_lsrscan_data,
            "rgbdlsr"   : get_rgbd_lsr_data,
        }
        func = switcher.get(arg, lambda: "Invalid argument")

        df = func()

        return df

    def id2name(self, id, arg='r'):
        """Doc string"""

        def get_home_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_homes
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_home_session_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_home_sessions
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_room_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_rooms
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_sensor_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_sensors
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_room_type_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_room_types
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_sensor_type_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_sensor_types
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_object_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_objects
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_object_type_name():
            """ Docstring """
            sql_str = (
                f'''
                select name
                from rh_object_types
                where id = {id}
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)


        switcher = {
            "h"            : get_home_name,
            "hs"           : get_home_session_name,
            "r"            : get_room_name,
            "rt"           : get_room_type_name,
            "s"            : get_sensor_name,
            "st"           : get_sensor_type_name,
            "o"            : get_object_name,
            "ot"           : get_object_type_name,
            "home"         : get_home_name,
            "home_session" : get_home_session_name,
            "room"         : get_room_name,
            "room_type"    : get_room_type_name,
            "sensor"       : get_sensor_name,
            "sensor_type"  : get_sensor_type_name,
            "object"       : get_object_name,
            "object_type"  : get_object_type_name,

        }
        func = switcher.get(arg, lambda: "Invalid argument")

        return func().iat[0,0]

    def name2id(self, name, arg='r'):
        """Doc string"""

        def get_home_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_homes
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_home_session_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_home_sessions
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_room_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_rooms
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_sensor_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_sensors
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_room_type_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_room_types
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_sensor_type_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_sensor_types
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_object_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_objects
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)

        def get_object_type_id():
            """ Docstring """
            sql_str = (
                f'''
                select id
                from rh_object_types
                where name like '%{name}%'
                '''
            )
            logger.debug(sql_str)
            return self.query(sql_str)


        switcher = {
            "h"            : get_home_id,
            "hs"           : get_home_session_id,
            "r"            : get_room_id,
            "rt"           : get_room_type_id,
            "s"            : get_sensor_id,
            "st"           : get_sensor_type_id,
            "o"            : get_object_id,
            "ot"           : get_object_type_id,
            "home"         : get_home_id,
            "home_session" : get_home_session_id,
            "room"         : get_room_id,
            "room_type"    : get_room_type_id,
            "sensor"       : get_sensor_id,
            "sensor_type"  : get_sensor_type_id,
            "object"       : get_object_id,
            "object_type"  : get_object_type_id,

        }
        func = switcher.get(arg, lambda: "Invalid argument")

        return func().iat[0,0]


    """
    RGBD data
    """
    def get_RGBD_files(self, id):
        """ Docstring """
        sql_str = (
            f'''
            select
              new_path as local_path,
              new_file_2 as rgb_file,
              new_file_1 as depth_file
            from rh2_old2new_rgbd_files
            where id = {id}
            '''
        )
        logger.debug(sql_str)
        # self.query(sql_str).values.flatten().tolist()
        # self.query(sql_str).loc[0,:].tolist()
        logger.debug('rh_rgbd_path: {}', self.__rgbd_path)
        files_path = self.query(sql_str).loc[0,:].tolist()
        depth_file = os.path.join(self.__rgbd_path, files_path[0], files_path[2])
        rgb_file = os.path.join(self.__rgbd_path, files_path[0], files_path[1])
        return [rgb_file, depth_file]

    def __get_RGBD_labels(self, id):
        """
        This function return a dataframe with labels for the observations
        referenced by id

        SQL query

        select * from rh_lblrgbd_labels
            where sensor_observation_id = id

        Parameters
        ----------
        id : int
            The primary key value to identify a row in the table
            rh_lbl_rgbd_labels.

        Returns
        -------
        A dataframe with the query result. An empty dataframe is returned when
        no rows are available, i.e., when the sensor observation does not
        belong to rh_lblrgbd (labelled rgbd)
        """
        sql_str = (
            f'''
            select *
            from rh_lblrgbd_labels
             where sensor_observation_id = {id}
            '''
        )
        logger.debug(sql_str)
        return self.query(sql_str)

    def __get_Labels_file(self, id):
        """
        Returns the <id>_labels.txt full path filename
        """
        sql_str = (
            f'''
            select
              new_path as local_path,
              new_file_3 as labels_file
            from rh2_old2new_rgbd_files
            where id = {id}
            '''
        )
        logger.debug(sql_str)
        files_path = self.query(sql_str).loc[0,:].tolist()
        labels_file = os.path.join(self.__rgbd_path, files_path[0], files_path[1])
        return labels_file

    def __get_label_mask_array(self, l_f):
        """
        Returns a numpy array from the <id>_labels.txt
        """
        mask = []
        with open(l_f, "r") as file_handler:
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

        # logger.debug("mask height: {}", len(mask))
        # logger.debug("mask width : {}", len(mask[0]))

        mask_array = np.array(mask)
        mask_array = np.rot90(mask_array)

        logger.debug("\nmask array size: {} (# rows, # cols)", mask_array.shape)
        logger.debug("\nmask array max value: {}", np.amax(mask_array))

        return mask_array

    def __decompose_label_mask_array(self, label_mask_array, labels):
        """
        Returns a list of binary 2D numpy.ndarray arrays (pixels being 1s and 0s)
        A 2D numpy.ndarray array per label

        Input
        =====
        label_mask_array: a numpy.ndarray of numpy.int64 values
                    Each value of the matrix must represents a pixel by means
                    of an int64. This number must be interpreted as a binary
                    number where each bit with value 1 means that the element
                    belongs to the label which label_id matchs the bit position.
                    For example, if an element has the value 1010, this means
                    that it belongs to the labels with id 1 and 3.
                    In this way an element can belong to more than one label. 

        labels: a pandas series with the 'local_id' column of a
                rh_lblrgbd_labels dataframe for a rh_lblrgbd record. This
                series always is a sequence of number in the range 1 to number
                of labels, i.e. 1,2,...,# labels

        Output
        ======
        masks: a 1-column dataframe of 2D binary arrays. Each item is a 2D binary
               numpy.nparray (pixels being 1s and 0s) corresponding to a label,
               where each matrix value <numpy.int8> corresponds to a pixel,
               being 1 if belongs to the label and 0 otherwise.
        """

        masks = []
        for label in labels:
            arr = label_mask_array & (2**(label))
            np.clip(arr, 0, 1, out=arr)
            arr = np.uint8(arr[:,2:-2])
            masks.append(arr)
        logger.debug("\nmask list with {} items of {} binary arrays", len(masks), masks[0].shape)

        # Transform masks list to a one-column pandas dataframe
        mask_df = pd.DataFrame(columns=['mask'])
        mask_df['mask'] = mask_df['mask'].astype(object)
        mask_df.loc[:, 'mask'] = masks
        return mask_df

    def get_RGBD_labels(self, id, masks = True):
        """
        Returns a list of one binary array per label of the RGBD image
        referenced by its id
        """
        # Get a dataframe from rh_lblrgbd_labels with labels of the id
        labels = self.__get_RGBD_labels(id)

        # By default 2D binary masks column is added to the labels dataframe
        if masks:
            # Get the <id>_labels.txt full path filename
            l_f = self.__get_Labels_file(id)
            # Get the label_mask_array from the <id>_labels.txt file
            label_mask_array = self.__get_label_mask_array(l_f)
            # logger.debug("\nlabels['local_id']: \n{}", labels['local_id'])
            # Get a 1-column dataframe of one binary array per label
            label_masks = self.__decompose_label_mask_array(label_mask_array, labels['local_id'])
            # Return the labels dataframe concatenated with the new label_masks
            # 1-column dataframe
            labels = pd.concat([labels, label_masks], axis=1)

        return labels


    """
    Laser Scanner data
    """
    def get_laser_scan(self,id):
        """
        This function return a dataframe with a laser scan for
        the observation referenced by id

        SQL query

        select * from rh_lsrscan_scans
            where sensor_observation_id = id

        Parameters
        ----------
        id : int
            The primary key value to identify a row in the table
            rh_lbl_rgbd_labels.

        Returns
        -------
        A dataframe with the query result. An empty dataframe is returned when
        no rows are available, i.e., when the sensor observation does not
        belong to rh_lblrgbd (labelled rgbd)
        """

        # if id < 200000:
        #     scan_table_name = 'rh_scans'
        # else:
        #     scan_table_name = 'rh_lsrscan_scans'

        scan_table = lambda id: 'rh_raw_scans' if id < 200000 else 'rh_lsrscan_scans'

        sql_str = (
            f'''
            select *
            from {scan_table(id)}
             where sensor_observation_id = {id}
            '''
        )
        logger.debug(sql_str)

        df = self.query(sql_str)

        # Laser scanner aperture and max distance are hard coded as it's in the
        # original dataset. Nevertheless are included as columns in the
        # rh2_sensor_observations
        df.aperture = 4.1847
        df.max_range = 5.6
        df.no_of_shots = 682

        return df


    """
    Scenes
    """
    def get_scenes(self):
        """
        Return a dataframe with scenes
        """
        sql_str = (
            f'''
            select
              rh_lblscene.id,
              home_session_id, home_subsession_id, home_id, room_id,
              '{self.__scene_path}' || '/' || new_path || '/' || new_file as scene_file
            from rh_lblscene
            inner join rh2_old2new_scene_files on rh_lblscene.id = rh2_old2new_scene_files.id
            '''
        )
        logger.debug(sql_str)
        scenes = self.query(sql_str)
        return scenes

    def get_scene_labels(self, id, obj=False):
        """
        This function return a dataframe with a laser scan for
        the observation referenced by id

        SQL query

        select * from rh_lsrscan_scans
            where sensor_observation_id = id

        Parameters
        ----------
        id : int
            The primary key value to identify a row in the table
            rh_lbl_rgbd_labels.

        Returns
        -------
        A dataframe with the query result. An empty dataframe is returned when
        no rows are available, i.e., when the sensor observation does not
        belong to rh_lblrgbd (labelled rgbd)
        """

        # if id < 200000:
        #     scan_table_name = 'rh_scans'
        # else:
        #     scan_table_name = 'rh_lsrscan_scans'

        labels_table = lambda obj: 'rh2_scene_bb_objects' if obj else 'rh_lblscene_bboxes'

        if obj:
            sql_str = (
                f'''
                select
                    id,
                    local_id,
                    scene_id,
                    object_id,
                    object_name,
                    object_type_id,
                    bb_pose_x,
                    bb_pose_y,
                    bb_pose_z,
                    bb_pose_yaw,
                    bb_pose_pitch,
                    bb_pose_roll,
                    bb_corner1_x,
                    bb_corner1_y,
                    bb_corner1_z,
                    bb_corner2_x,
                    bb_corner2_y,
                    bb_corner2_z,
                    planarity,
                    scatter,
                    linearity,
                    min_height,
                    max_height,
                    centroid_x,
                    centroid_y,
                    centroid_z,
                    volume,
                    biggest_area,
                    orientation,
                    hue_mean,
                    saturation_mean,
                    value_mean,
                    hue_stdv,
                    saturation_stdv,
                    value_stdv,
                    hue_histogram_0,
                    hue_histogram_1,
                    hue_histogram_2,
                    hue_histogram_3,
                    hue_histogram_4,
                    value_histogram_0,
                    value_histogram_1,
                    value_histogram_2,
                    value_histogram_3,
                    value_histogram_4,
                    saturation_histogram_0,
                    saturation_histogram_1,
                    saturation_histogram_2,
                    saturation_histogram_3,
                    saturation_histogram_4
                from {labels_table(obj)}
                where scene_id = {id}
                '''
            )
        else:
            sql_str = (
                f'''
                select *
                from {labels_table(obj)}
                where scene_id = {id}
                '''
            )

        logger.debug(sql_str)
        df = self.query(sql_str)
        return df


    """
    Observations
    """

    def get_observations(self):
        """
        Return a dataframe with observations
        """
        sql_str = (
            f'''
            select *
            from rh_observations
            '''
        )
        logger.debug(sql_str)
        observations = self.query(sql_str)
        return observations

    def get_objects_in_observation(self, id):
        """
        Return a dataframe with objects in observation
        """
        sql_str = (
            f'''
            select rh_objects.*
            from rh_objects_in_observation
            inner join rh_objects on rh_objects_in_observation.object_id == rh_objects.id
            where  rh_objects_in_observation.observation_id == {id}
            '''
        )
        logger.debug(sql_str)
        objects = self.query(sql_str)
        return objects

    def get_objects(self):
        """
        Return a dataframe with objects
        """
        sql_str = (
            f'''
            select *
            from rh_objects
            '''
        )
        logger.debug(sql_str)
        objects = self.query(sql_str)
        return objects

    def get_object_relations(self, id=None):
        """
        Return a dataframe with object relationships
        """

        sql_str = (
            f'''
            select *
            from rh_relations
            '''
        )

        where_str = (
            f'''
            where obj1_id == {id} or obj2_id == {id}
            '''
        )

        if (id is not None):
            sql_str = sql_str + where_str

        logger.debug(sql_str)
        object_relations = self.query(sql_str)
        return object_relations


    """
    Stuff
    """

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

        sensor_observation_table = self.__aliases[source]

        # Just to doc a cumbersone alternative code:
        #
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
        #     from rh_lblrgbd_temp
        #     where id = {}
        #     '''.format(so_id)
        # )

        sql_str = (
            f'''
            select pth, f3
            from rh_lblrgbd_temp
            where id = {so_id}
            '''
        )

        df_rows = pd.read_sql_query(sql_str, self.__con)
        logger.debug("df_rows.shape: {}", df_rows.shape)
        # print(df_rows)
        # print(df_rows.loc[0,"pth"])
        # print(df_rows.loc[0,"f3"])
        label_path_file_name = os.path.join(self.__rgbd_path,
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

    def get_object_type_names(self):
        """
        Return a list with room type names
        """
        return self.select_column('name', 'rh_object_types')


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


    """
    Just for reference.
    Don't use any of them.
    To remove in the near future
    """

    def __create_temp_views_back(self):
        """
        This function creates temporary views to work on the class environment
        """

        sql_str = '''
        begin transaction;
        drop view if exists rh_lblrgbd_temp
        create temp view rh_lblrgbd_temp as
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

        self.__aliases.append("rh_lblrgbd_temp")
        logger.trace("The view rh_lblrgbd_temp has been created")

    def __get_sql_string_for_rgbd_tables(self, table_name):
        sql_str = (f'''
        begin transaction;
        drop view if exists {table_name}_temp;
        create temp view {table_name}_temp as
        select
            {table_name}.id,
            {table_name}.home_session_id as hs_id,
            rh_home_sessions.name as hs_name,
            {table_name}.home_subsession_id as hss_id,
            {table_name}.home_id as h_id,
            rh_homes.name as h_name,
            {table_name}.room_id as r_id,
            rh_rooms.name as r_name,
            {table_name}.sensor_id as s_id,
            rh_sensors.name as s_name,
            {table_name}.time_stamp as t,
            {table_name}.sensor_pose_x as s_px,
            {table_name}.sensor_pose_y as s_py,
            {table_name}.sensor_pose_z as s_pz,
            {table_name}.sensor_pose_yaw as s_pya,
            {table_name}.sensor_pose_pitch as s_ppi,
            {table_name}.sensor_pose_roll as s_pro,
            rh2_old2new_rgbd_files.new_file_1 as f1,
            rh2_old2new_rgbd_files.new_file_2 as f2,
            rh2_old2new_rgbd_files.new_file_3 as f3,
            rh2_old2new_rgbd_files.new_path as pth
        from {table_name}
        inner join rh_home_sessions on home_session_id = rh_home_sessions.id
        inner join rh_homes on {table_name}.home_id = rh_homes.id
        inner join rh_rooms on {table_name}.room_id = rh_rooms.id
        inner join rh_sensors on {table_name}.sensor_id = rh_sensors.id
        inner join rh2_old2new_rgbd_files on rh2_old2new_rgbd_files.id = {table_name}.id;
        commit;
        ''')

        return sql_str

    def __get_sql_string_for_scan_tables(self, table_name):
        sql_str = (f'''
        begin transaction;
        drop view if exists {table_name}_temp;
        create temp view {table_name}_temp as
        select
            {table_name}.id,
            {table_name}.home_session_id as hs_id,
            rh_home_sessions.name as hs_name,
            {table_name}.home_subsession_id as hss_id,
            {table_name}.home_id as h_id,
            rh_homes.name as h_name,
            {table_name}.room_id as r_id,
            rh_rooms.name as r_name,
            {table_name}.sensor_id as s_id,
            rh_sensors.name as s_name,
            {table_name}.time_stamp as t,
            {table_name}.sensor_pose_x as s_px,
            {table_name}.sensor_pose_y as s_py,
            {table_name}.sensor_pose_z as s_pz,
            {table_name}.sensor_pose_yaw as s_pya,
            {table_name}.sensor_pose_pitch as s_ppi,
            {table_name}.sensor_pose_roll as s_pro,
        	NULL as f1,
			NULL as f2,
			NULL as f3,
            NULL as pth
        from {table_name}
        inner join rh_home_sessions on home_session_id = rh_home_sessions.id
        inner join rh_homes on {table_name}.home_id = rh_homes.id
        inner join rh_rooms on {table_name}.room_id = rh_rooms.id
        inner join rh_sensors on {table_name}.sensor_id = rh_sensors.id;
        commit;
        ''')

        return sql_str

    def __get_sql_string_for_raw_tables(self, table_name):
        sql_str = (f'''
        begin transaction;
        drop view if exists {table_name}_temp;
        create temp view {table_name}_temp as
        select
            {table_name}.id,
            {table_name}.home_session_id as hs_id,
            rh_home_sessions.name as hs_name,
            {table_name}.home_subsession_id as hss_id,
            {table_name}.home_id as h_id,
            rh_homes.name as h_name,
            {table_name}.room_id as r_id,
            rh_rooms.name as r_name,
            {table_name}.sensor_id as s_id,
            rh_sensors.name as s_name,
            {table_name}.time_stamp as t,
            {table_name}.sensor_pose_x as s_px,
            {table_name}.sensor_pose_y as s_py,
            {table_name}.sensor_pose_z as s_pz,
            {table_name}.sensor_pose_yaw as s_pya,
            {table_name}.sensor_pose_pitch as s_ppi,
            {table_name}.sensor_pose_roll as s_pro,
            rh2_old2new_rgbd_files.new_file_1 as f1,
            rh2_old2new_rgbd_files.new_file_2 as f2,
            rh2_old2new_rgbd_files.new_file_3 as f3,
            rh2_old2new_rgbd_files.new_path as pth
        from {table_name}
        inner join rh_home_sessions on home_session_id = rh_home_sessions.id
        inner join rh_homes on {table_name}.home_id = rh_homes.id
        inner join rh_rooms on {table_name}.room_id = rh_rooms.id
        inner join rh_sensors on {table_name}.sensor_id = rh_sensors.id
        left join rh2_old2new_rgbd_files on rh2_old2new_rgbd_files.id = {table_name}.id;
        commit;
        ''')

        return sql_str

    def __create_temp_views(self):
        """
        This function creates temporary views to work on the class environment
        """

        queries = []

        # Creating view rh_raw_temp
        table_alias = 'raw'
        table_name = 'rh_raw'
        queries.append(self.__get_sql_string_for_raw_tables(table_name))
        self.__aliases[table_alias] = table_name + '_temp'

        # Creating view rh_rgbd_temp
        table_alias = 'rgbd'
        table_name = 'rh_rgbd'
        queries.append(self.__get_sql_string_for_rgbd_tables(table_name))
        self.__aliases[table_alias] = table_name + '_temp'

        # Creating view rh_lblrgbd_temp
        table_alias = 'lblrgbd'
        table_name = 'rh_lblrgbd'
        queries.append(self.__get_sql_string_for_rgbd_tables(table_name))
        self.__aliases[table_alias] = table_name + '_temp'

        # Creating view rh_lsrscan_temp
        table_alias = 'lsrscan'
        table_name = 'rh_lsrscan'
        queries.append(self.__get_sql_string_for_scan_tables(table_name))
        self.__aliases[table_alias] = table_name + '_temp'

        for query in queries:
            self.query(query, False)

    def get_aliases(self):
        """
        Return a dictionary with table/view aliases 
        """

        return self.__aliases

    def get_names_of_sensor_data_tables(self):
        """
        Return a list of friendly names from sensor observation tables
        """
        return list(self.get_aliases().keys())

    def get_sensor_data(self, source='lblrgbd'):
        """
        This functions queries the database to extract sensor observation
        data.
        """

        # Get a cursor to execute SQLite statements
        cur = self.__con.cursor()

        sensor_observation_table = self.__aliases[source]

        sql_str = (
            f'''
            select *
            from {sensor_observation_table}
            order by t
            '''
        )
        logger.debug(sql_str)

        df = pd.read_sql_query(sql_str, self.__con)

        return df

