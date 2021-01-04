#!/usr/bin/env python
import sys
import traceback

class KT:
    APP = None
    PACKED = None
    # ^ ONLY the window frame widget (whose parent is APP a.k.a. root)
    #   is packed. Everything else uses grid.
    indent = ""


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
