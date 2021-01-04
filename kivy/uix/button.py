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
from kivy.properties import ListProperty


class Button(ttk.Button, Label):

    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        if self.parent is not None:
            self.finalize()
        # print("The parent of a Button is {}".format(self.parent))

        # self.text(".")  # this should not work
        # self.text = "..."  # this should work

    def finalize(self):
        if self.parent is None:
            raise RuntimeError("[kivy-tkinter]"
                               " kivy-tkinter failed to set a parent"
                               " before calling {}.finalize."
                               "".format(type(self).__name__))
        ttk.Button.__init__(self, self.parent,
                            textvariable=self._sv)
        self.children = ListProperty(self.children)
        # ^ coerce Tkinter to use a ListProperty
        #   (kivy-tkinter's ListProperty is adaptive so dict-like
        #   behavior used by Tkinter should work)

    def bind(self, **kwargs):
        Label.bind(self, **kwargs)
