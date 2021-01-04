#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.uix.widget import Widget

class Label(ttk.Label, Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        ttk.Label.__init__(self, self.parent)
        # print("The parent of a Label is {}".format(self.parent))

    def bind(self, **kwargs):
        Widget.bind(self, **kwargs)
