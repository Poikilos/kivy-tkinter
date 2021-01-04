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

class Label(tk.Message, Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        tk.Message.__init__(self, self.parent, textvariable=self._sv)
        # ^ ttk.Label doesn't have multiple lines
        # ^ tk.Message has multiple lines
        # ^ tk.Text has multiple fonts
        # print("The parent of a Label is {}".format(self.parent))

    def bind(self, **kwargs):
        Widget.bind(self, **kwargs)
