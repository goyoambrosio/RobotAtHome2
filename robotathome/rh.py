#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/11/19"
__license__ = "MIT"

import fire
from robotathome.dataset import Dataset


def rh(*args):
    rhds = Dataset("MyRobot@Home")
    # print(args[0])
    if args[0] == 'install':
        if (len(args[1:] == 0)):
            
        print(len(args[1:]))


def main():
    """
    Multiline comment

    """
    try:
        fire.Fire(rh)
    except:
        print('A command must be provided')


if __name__ == "__main__":
    main()
