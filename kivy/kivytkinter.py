#!/usr/bin/env python
import sys
import traceback

class KT:
    APP = None
    indent = ""


def warn(msg):
    # sys.stderr.write("{}\n".format(msg))
    print(msg)

def view_traceback(indent=""):
    ex_type, ex, tb = sys.exc_info()
    print(indent+str(ex_type))
    print(indent+str(ex))
    traceback.print_tb(tb)
    del tb
