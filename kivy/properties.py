#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk


class DictProperty:

    def __init__(self, *args):
        if len(args) == 1:
            for k,v in args[0].items():
                self[k] = v
        elif len(args) > 1:
            raise ValueError("Only 0-1 arguments are implemented for"
                             " DictProperty.")

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]


class ListProperty:
    def __init__(self, *args):
        raise NotImplementedError


class NumericProperty:
    def __init__(self, *args):
        raise NotImplementedError


class ObjectProperty:
    def __init__(self, *args):
        raise NotImplementedError


class StringProperty:
    def __init__(self, *args):
        raise NotImplementedError

