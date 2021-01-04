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
from kivy.kivytkinter import view_traceback
from kivy.kivytkinter import error
from kivy.properties import ListProperty


class BoxLayout(ttk.Frame, Layout):

    def __init__(self, **kwargs):
        Layout.__init__(self, **kwargs)
        # super(BoxLayout, self).__init__(**kwargs)
        # TODO: implement spacing, padding, children, orientation,
        # parent, size, pos
        self.gm = "grid"  # which Tkinter geometry manager to use
        self._layoutI = 0

        self.orientation = kwargs.get("orientation", "horizontal")
        if "orientation" in kwargs:
            del kwargs["orientation"]

        if self.parent is not None:
            self.finalize()
        # print("The parent of a BoxLayout is {} and the orientation is"
        # #     " {}".format(self.parent, self.orientation))

    def finalize(self):
        if self.parent is None:
            raise RuntimeError("[kivy-tkinter]"
                               " kivy-tkinter failed to set a parent"
                               " before calling {}.finalize."
                               "".format(type(self).__name__))
        ttk.Frame.__init__(self, self.parent)
        self.children = ListProperty(self.children)
        # ^ coerce Tkinter to use a ListProperty
        #   (kivy-tkinter's ListProperty is adaptive so dict-like
        #   behavior used by Tkinter should work)

    def add_widget(self, widget, index=0, canvas=None):
        if widget.parent is None:
            # It must have been generated in Python.
            widget.parent = self
            widget.finalize()
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
            widget.atI = self._layoutI
            row = None
            column = None
            try:
                if self.orientation == "horizontal":
                    row = 0
                    column = self._layoutI
                    widget.grid(column=column, row=row,
                                sticky=tk.NSEW) # sticky=tk.N+tk.S)
                elif self.orientation == "vertical":
                    row = self._layoutI
                    column = 0
                    widget.grid(column=column, row=row,
                                sticky=tk.NSEW) # sticky=tk.W+tk.E)
                else:
                    raise ValueError(
                        "Unknown Kivy orientation: {} '{}'"
                        "".format(type(self.orientation).__name__,
                                  self.orientation)
                    )
                tk.Grid.rowconfigure(widget.parent, row, weight=1)
                tk.Grid.columnconfigure(widget.parent, column, weight=1)
                # ^ expand
                widget._last_gm = 'grid'
            except tk.TclError as ex:
                view_traceback()
                error("The parent {} of {} {} is a {}".format(
                    self.parentId(),
                    type(self).__name__,
                    self.id,
                    type(self.parent).__name__,
                ))
                raise RuntimeError("[kivy-tkinter kivy.uix.boxlayout]"
                                   " If grid failed due to"
                                   " using pack, the item should be a"
                                   " grid but kivy-tkinter failed to"
                                   " ensure that (Tkinter says: {}"
                                   ").".format(ex))
            self._layoutI += 1
        else:
            raise ValueError("A Tkinter geometry manager named {} is"
                             " not implemented.".format(self.gm))
        self.children.append(widget)
