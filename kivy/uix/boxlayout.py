#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk


__all__ = ('BoxLayout', )

from kivy.kivytkinter import KT
from kivy.uix.layout import Layout

class BoxLayout(ttk.Frame, Layout):

    def __init__(self, **kwargs):
        Layout.__init__(self, **kwargs)
        # super(BoxLayout, self).__init__(**kwargs)
        # TODO: implement spacing, padding, children, orientation,
        # parent, size, pos
        self.gm = "grid"  # which Tkinter geometry manager to use
        self.layoutI = 0

        self.orientation = kwargs.get("orientation", "horizontal")
        if "orientation" in kwargs:
            del kwargs["orientation"]

        ttk.Frame.__init__(self, self.parent)
        # print("The parent of a BoxLayout is {} and the orientation is"
        # #     " {}".format(self.parent, self.orientation))

    def add_widget(self, widget, index=0, canvas=None):
        # TODO: implement pos_hint
        pre = "[BoxLayout add_widget] "
        if index != 0:
            warn(pre + "index is not implemented.")
        if canvas is not None:
            warn(pre + "canvas is not implemented.")
        if not hasattr(self, 'gm'):
            raise AttributeError("The BoxLayout must define a"
                                 " Tkinter geometry manager.")
        if self.gm == "grid":
            '''
            print(KT.indent + "+adding a {} to a {}..."
                  "".format(type(widget).__name__,
                            type(self).__name__))
            '''
            widget.atI = self.layoutI
            if self.orientation == "horizontal":
                widget.grid(column=self.layoutI, row=0,
                            sticky=tk.N+tk.S)
            elif self.orientation == "vertical":
                widget.grid(column=0, row=self.layoutI,
                            sticky=tk.W+tk.E)
            else:
                raise ValueError(
                    "Unknown Kivy orientation: {} '{}'"
                    "".format(type(self.orientation).__name__,
                              self.orientation)
                )
            self.layoutI += 1
        else:
            raise ValueError("A Tkinter geometry manager named {} is"
                             " not implemented.".format(self.gm))
