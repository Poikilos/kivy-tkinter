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
from kivy.properties import ListProperty


class Label(tk.Message, Widget):

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        if self.parent is not None:
            self.finalize()
        # print("The parent of a Label is {}".format(self.parent))

    def finalize(self):
        if self.parent is None:
            raise RuntimeError("[kivy-tkinter]"
                               " kivy-tkinter failed to set a parent"
                               " before calling {}.finalize."
                               "".format(type(self).__name__))
        tk.Message.__init__(self, self.parent, textvariable=self._sv)
        # ^ ttk.Label doesn't have multiple lines
        # ^ tk.Message has multiple lines
        # ^ tk.Text has multiple fonts
        self.children = ListProperty(self.children)
        # ^ coerce Tkinter to use a ListProperty
        #   (kivy-tkinter's ListProperty is adaptive so dict-like
        #   behavior used by Tkinter should work)

    def bind(self, **kwargs):
        Widget.bind(self, **kwargs)
