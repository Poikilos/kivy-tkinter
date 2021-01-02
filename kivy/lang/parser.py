#!/usr/bin/env python

import importlib

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.lang import Builder

class Parser:

    def __init__(self, **kwargs):
        self.root = None
        self.sourcecode = []
        self.filename = kwargs.get('filename', None)
        content = kwargs.get('content', None)
        if content is None:
            raise ValueError('No content passed')
        self.parse(content)

    def parse(self, content):
        self.sourcecode = content.split("\n")

    @staticmethod
    def kvCommand(self, line):
        aoi = line.find(":")
        if aoi < 0:
            raise ValueError("Missing ':' in \"{}\"".format(line))
        result = {
            left: line[:aoi].strip(),
            right: line[aoi+1:].strip(),
            className: None,
        }
        if result.right.startswith("#"):
            result.right = None
        elif len(result.right) == 0:
            result.right = None
        if left.startswith("<"):
            if not left.endswith(">"):
                raise ValueError("Missing '>' in {}".format(line))
            result.className = left[1:-1]
        return result

