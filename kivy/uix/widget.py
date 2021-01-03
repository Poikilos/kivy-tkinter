#!/usr/bin/env python

# import warnings

__all__ = ('Widget', 'WidgetException')

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.kivytkinter import APP
from kivy.kivytkinter import warn

class Widget:

    def __init__(self, **kwargs):
        self.parent = None
        if "tkinterParent" in kwargs:
            self.parent = kwargs["tkinterParent"]
            del kwargs["tkinterParent"]
        if self.parent is None:
            self.parent = APP.ROOT

class WidgetException(Exception):
    pass
