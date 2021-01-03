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

class TextInput(ttk.Entry, Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        self._sv = tk.StringVar()
        # TODO: in Kivy, a subclass of any given widget subclass would
        # require setting text to "root.sv" in KV, where sv was a
        # StringProperty in the subclass.
        ttk.Entry.__init__(self, self.parent, textvariable=self._sv)
        if 'text' in kwargs:
            self.sv.set(kwargs['text'])
        print("The parent of a Label is {}".format(self.parent))

    @property
    def text(self):
        return self._sv.get()

    @text.setter
    def text(self, value):
        self._sv.set(value)
