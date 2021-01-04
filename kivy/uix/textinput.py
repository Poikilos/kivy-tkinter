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
        # TODO: in Kivy, a subclass of any given widget subclass would
        # require setting text to "root.sv" in KV, where sv was a
        # StringProperty in the subclass.
        if 'text' in kwargs:
            self.sv.set(kwargs['text'])
        # print("The parent of a Label is {}".format(self.parent))
        if self.parent is not None:
            self.finalize()

    def finalize(self):
        if self.parent is None:
            raise RuntimeError("[kivy-tkinter]"
                               " kivy-tkinter failed to set a parent"
                               " before calling {}.finalize."
                               "".format(type(self).__name__))
        ttk.Entry.__init__(self, self.parent, textvariable=self._sv)
