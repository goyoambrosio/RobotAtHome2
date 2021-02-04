#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2021, Gregorio Ambrosio"
__date__ = "2021/02/03"
__license__ = "MIT"

import sys
import fire
from robotathome.dataset import Dataset


# =========================
#      GLOBAL VARIABLES
# =========================
# Dataset
RHDS = None


def downcheck(path=".", dataunit="all"):

    """ Docstring """

    global RHDS

    RHDS = Dataset("MyRobot@Home", path, autoload=False)

    if dataunit == "all":
        dataunit_names = ["chelmnts",
                          "2dgeomap",
                          "hometopo",
                          "raw",
                          "lsrscan",
                          "rgbd",
                          "lblrgbd",
                          "lblscene",
                          "rctrscene"]
        for dataunit_name in dataunit_names:
            process_unit(dataunit_name)
    else:
        try:
            process_unit(dataunit)
        except Exception as e:
            print("Oops! ", sys.exc_info()[0], " occurred in: ", dataunit_name)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


    print(RHDS)


def process_unit(dataunit):

    """ Docstring """

    RHDS.unit[dataunit].load_data()
    # print(RHDS.unit[dataunit])
    RHDS.unit[dataunit].check_folder_size(True)


def main():

    """ Docstring """

    fire.Fire(downcheck)

    # main return
    return 0


if __name__ == "__main__":
    main()

