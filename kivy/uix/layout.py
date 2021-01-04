#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

__all__ = ('Layout', )

from kivy.uix.widget import Widget


class Layout(Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        # print("(The parent of a Layout is {})".format(self.parent))
