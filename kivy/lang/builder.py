#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk


class Builder:

    _loadedStr = ""

    @staticmethod
    def load_string(kvStr):
        Builder._loadedStr = kvStr

    @staticmethod
    def load(path):
        with open(path, 'r') as ins:
            for line in ins:
                _loadedStr += line.rstrip() + "\n"
