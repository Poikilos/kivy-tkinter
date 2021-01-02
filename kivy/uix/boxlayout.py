#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.app import App
from kivy.uix import Widget

class BoxLayout(tk.Frame, Widget):
    
    def __init__(self, **kwargs):
        self.gm = "grid"  # which Tkinter geometry manager to use
        self.orientation = kwargs.get("orientation", "horizontal")
        self.layoutI = 0
        if kwargs.has_key("orientation"):
            del kwargs["orientation"]
        tk.Frame().__init__(App.ROOT, **kwargs)

    
