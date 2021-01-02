#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.lang.builder import Builder
from kivy.lang.parser import Parser

__all__ = ('Builder', 'Parser')


# TODO:
#from kivy.lang.builder import (Observable, Builder, BuilderBase,
#                               BuilderException)
#from kivy.lang.parser import Parser, ParserException, global_idmap
#
#__all__ = ('Observable', 'Builder', 'BuilderBase', 'BuilderException',
#           'Parser', 'ParserException', 'global_idmap')
