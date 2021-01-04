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
from kivy.properties import DictProperty
from kivy.properties import ListProperty

class Widget:
    ids = DictProperty({})

    def __init__(self, **kwargs):
        self.id = None
        self._sv = tk.StringVar()
        self._opacity = 1.0
        self._last_gm = None
        self._size_hint = (1.0, 1.0)
        self.children = ListProperty([])

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
            if KT.PACKED is not None:
                '''
                raise RuntimeError("[kivy-tkinter kivy.uix.widget]"
                                   " The parent is None but there is"
                                   " already a main form.")
                '''
                # self.parent = KT.APP.frame
                # That's ok, we can auto-detect that in add_widget.
            else:
                self.parent = KT.APP

    def bind(self, **kwargs):
        on_press = kwargs.get('on_press')
        if on_press is not None:
            self.configure(command=on_press)
            '''
            print(KT.indent + "command for {} is now a {}"
                  "".format(self.id, type(on_press).__name__))
            '''
        else:
            raise NotImplementedError("{} is not implemented."
                                      "".format(kwargs))

    def finalize(self):
        raise RuntimeError("You must implement finalize in each"
                           " widget subclass in kivy-tkinter.")

    @property
    def text(self):
        return self._sv.get()

    @text.setter
    def text(self, value):
        '''
        print("Setting text for {} to \"{}\".".format(
            type(self).__name__,
            value,
        ))
        '''
        self._sv.set(value)

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):

        if self.parent.gm == 'grid':
            if value < 0.5:
                if self._opacity >= 0.5:
                    self.grid_remove()
                # grid_remove remembers the row and column, but
                # grid_forget does not.
            else:
                if self._opacity < 0.5:
                    if self._last_gm is None:
                        raise RuntimeError("The grid item is not marked"
                                           " as having been in a grid.")
                    self.grid()
        else:
            raise NotImplementedError("The Tkinter geometry manager {}"
                                      " used by {} id:{} is not"
                                      " implemented in kivy-tkinter."
                                      "".format(
                type(self.parent).__name__,
                self.parentId(),
                self.parent.gm,
            ))
            if value < 0.5:
                if self._opacity >= 0.5:
                    self.pack_forget()
            else:
                if self._opacity < 0.5:
                    self.pack()
        self._opacity = value

    @property
    def size_hint(self):
        return self._size_hint

    @size_hint.setter
    def size_hint(self, values):
        if len(values) != 2:
            raise ValueError("size_hint must have 2 values: (w, h) but"
                             " is {}".format(value))
        conv = [v for v in values]
        for i in range(len(values)):
            v = values[i]
            if isinstance(v, float):
                pass
            elif isinstance(v, int):
                conv[i] = float(v)
                # kivy-tkinter's KV parser will allow int if both
                # convert to int without ValueError, so convert back to
                # float in that case.
            else:
                print("{} is not implemented for size_hint values."
                      " Try float.")
        self._size_hint = tuple(conv)

    def parentId(self):
        if self.parent is not None:
            return self.parent.id
        return None


class WidgetException(Exception):
    pass