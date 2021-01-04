#!/usr/bin/env python
import sys
import traceback


class KT:
    '''
    Access important kivy-tkinter values.
    - APP: The root Tk object
    - FORM: This is the main form that is packed into APP (Tk root),
      which in Kivy is the widget returned by build (all other widgets
      are under this one, and use `grid()` not `pack()`.
    '''
    APP = None
    FORM = None
    indent = ""
    MIN_W = 400
    MIN_H = 300


def warn(msg):
    sys.stderr.write("Warning: {}\n".format(msg))
    print(msg)


def view_traceback(indent=""):
    ex_type, ex, tb = sys.exc_info()
    print(indent+str(ex_type))
    print(indent+str(ex))
    traceback.print_tb(tb)
    del tb


def error(msg):
    sys.stderr.write("ERROR: {}\n".format(msg))
