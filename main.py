#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is the docstring"""

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/04/17"
__license__ = "GPLv3"

import fire


def hello(name):
  return 'Hello {name}!'.format(name=name)


def main():

    # This isn’t technically a comment. It’s a string that’s not assigned to any
    # variable, so it’s not called or referenced by your program. Still, since
    # it’ll be ignored at runtime and won’t appear in the bytecode, it can
    # effectively act as a comment.

    """
    Multiline comment
    """

    # Single line comment

    english = 'Hello World'   # call python main.py english
    spanish = 'Hola Mundo'    # call python main.py spanish

    fire.Fire(hello)          # call python main.py --name Goyo

    return 0

if __name__ == "__main__":
    main()
