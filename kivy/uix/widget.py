#!/usr/bin/env python

# import warnings

__all__ = ('Widget', 'WidgetException')

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.kivytkinter import KT
from kivy.kivytkinter import warn


class Widget:

    def __init__(self, **kwargs):
        self.id = None
        self._sv = tk.StringVar()
        self._opacity = 1.0

        self.parent = None

        if "tkinterParent" in kwargs:
            self.parent = kwargs["tkinterParent"]
            del kwargs["tkinterParent"]

        for k,v in kwargs.items():
            if hasattr(self, k):
                self.__dict__[k] = v
            else:
                print("  - The `{}` property is not implemented."
                      "".format(k))

        if self.parent is None:
            self.parent = KT.APP

    def bind(self, **kwargs):
        on_press = kwargs.get('on_press')
        if on_press is not None:
            self.configure(command=on_press)
        else:
            raise NotImplementedError("{} is not implemented."
                                      "".format(kwargs))

    @property
    def text(self):
        return self._sv.get()

    @text.setter
    def text(self, value):
        self._sv.set(value)

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        if self.parent.gm == 'grid':
            if value < 0.5:
                self.grid_remove()
            else:
                self.grid()
        else:
            if value < 0.5:
                self.pack_forget()
            else:
                self.pack()


class WidgetException(Exception):
    pass
