#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home cruncher.py """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/01/13"
__license__ = "MIT"


import os
import shutil
import sys
import re
import sqlite3
import fire
import cv2


# =========================
#      GLOBAL VARIABLES
# =========================
# Database connection
CON = 0


def copy_rgbd_files(source_folder_path, rgbd_folder_path):

    """ Docstring """

    sql_str_select_rgbd_files = "SELECT * FROM rh2_old2new_rgbd_files;"
    cursor_obj = CON.cursor()
    cursor_obj.execute(sql_str_select_rgbd_files)
    rows = cursor_obj.fetchall()

    for row in rows:
        for i in [2, 3, 4]:
            if row[i]:
                if not os.path.exists(os.path.join(rgbd_folder_path, row[5])):
                    os.makedirs(os.path.join(rgbd_folder_path, row[5]))

                file_ext = re.search(r"\.([^.]+)$", row[i]).group(1)
                if file_ext == 'png':
                    img = cv2.imread(os.path.join(source_folder_path, row[1], row[i]), cv2.IMREAD_COLOR)
                    img_rot = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    cv2.imwrite(os.path.join(rgbd_folder_path, row[5], row[i+4]), img_rot)
                else:
                    shutil.copy(
                        os.path.join(source_folder_path, row[1], row[i]),
                        os.path.join(rgbd_folder_path, row[5], row[i+4])
                    )
        sys.stdout.write("\rProcessing rgbd row %d " % (rows.index(row)))
        sys.stdout.flush()
    print("\n")


def copy_scene_files(source_folder_path, scene_folder_path):

    """ Docstring """

    sql_str_select_rgbd_files = "SELECT * FROM rh2_old2new_scene_files;"
    cursor_obj = CON.cursor()
    cursor_obj.execute(sql_str_select_rgbd_files)
    rows = cursor_obj.fetchall()

    for row in rows:
        if not os.path.exists(os.path.join(scene_folder_path, row[2])):
            os.makedirs(os.path.join(scene_folder_path, row[2]))
        shutil.copy(
            os.path.join(source_folder_path, row[1]),
            os.path.join(scene_folder_path, row[2], row[3])
        )
        sys.stdout.write("\rProcessing scene row %d " % (rows.index(row)))
        sys.stdout.flush()
    print("\n")


def copy_files(db_name='rh.db', source_folder_path='.', target_folder_path='.'):

    """ Docstring """

    global CON

    # =====================
    #   SQLite initialize
    # =====================

    # global database connection
    CON = sql_connection(db_name)

    # Folder stuff
    rgbd_folder_path = os.path.join(target_folder_path, 'rgbd')
    scene_folder_path = os.path.join(target_folder_path, 'scene')

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)
    if not os.path.exists(rgbd_folder_path):
        os.makedirs(rgbd_folder_path)
    if not os.path.exists(scene_folder_path):
        os.makedirs(scene_folder_path)

    copy_rgbd_files(source_folder_path, rgbd_folder_path)
    copy_scene_files(source_folder_path, scene_folder_path)

    # =====================
    #  Closing connections
    # =====================
    CON.close()


def sql_connection(database_name):

    """ Docstring """

    global CON

    try:
        CON = sqlite3.connect(database_name)
        print("Connection is established: ", database_name)
        return CON

    except NameError:

        print(NameError)


def main():

    """ Docstring """

    fire.Fire(copy_files)

    # main return
    return 0


if __name__ == "__main__":
    main()
