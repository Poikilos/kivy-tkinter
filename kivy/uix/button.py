#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.uix.label import Label

class Button(ttk.Button, Label):

    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        ttk.Button.__init__(self, self.parent)
        print("The parent of a Button is {}".format(self.parent))
