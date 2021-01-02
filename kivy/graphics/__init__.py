#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk


class Canvas(tk.Canvas):
    raise NotImplementedError


class Color:
    raise NotImplementedError


class Rectangle:
    raise NotImplementedError


class Fbo:
    raise NotImplementedError


def ClearColor():
    raise NotImplementedError


def ClearBuffers(self):
    raise NotImplementedError
