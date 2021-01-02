#!/usr/bin/env python
import os
import inspect

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showerror
except ImportError:
    # python 2
    import Tkinter as tk
    import ttk
    from tkFileDialog import askopenfilename
    from tkMessageBox import showerror

#if os.path.isfile
from kivy.lang import Builder
from kivy.lang import Parser

class App(tk.Tk):
    IS_TKINTER = True
    ROOT = None

    def __init__(self):
        super().__init__()
        self.title = str(type(self))
        if self.title.endswith("App"):
            self.title = self.title[:-3]
    
    def run(self):
        self.parser = Parser(content=Builder._loadedStr)
        self._build()

    def load_kv(self, filename=None):
        appName = type(self).__name__
        if appName.endswith("App"):
            appName = appName[:-3]
        if filename is None:
            filename = appName.lower() + ".kv"
        if filename is None:
            return
        if not os.path.isfile(filename):
            print("There is no \"{}\".".format(filename))

    def _build(self):
        '''
        Construct the app from kv language lines if present. (Doing so
        here and now is likely not a Kivy-like way of doing things).
        '''
        indent = ""
        prevIndent = None
        stack = []
        # print("I am a {}.".format(str(type(self).__name__)))
        frame = inspect.stack()[2]
        cf = frame[0].f_code.co_filename
        mod = importlib.import_module(cf)
        # print("The file with custom widgets is \"{}\".".format(cf))
        App.ROOT = self
        self.frame = self.build()
        lineN = 0
        for i in range(len(self.parser.sourcecode)):
            lineN += 1
            line = self.parser.sourcecode[i].rstrip()
            lineS = line.strip()
            if lineS.startswith("#"):
                continue
            dent = line[:-(len(line)-len(lineS))]
            # if len(stack) == 0:
            kvc = Parser.kvCommand(lineS)
            deeperO = None
            if kvc.className != None:
                ThisClass = getattr(mod, kvc.className)
                deeperO = ThisClass()
            elif kvc.right is None:
                ThisClass = eval(kvc.left)
                deeperO = ThisClass()
            else:
                if len(stack) == 0:
                    fn = "kv in {}".format(cf)
                    if self.parser.filename is not None:
                        fn = self.parser.filename
                    raise SyntaxError("Line {} of {} has a variable"
                                      " before an object: {}"
                                      "".format(lineN, fn, line))
            raise NotImplementedError("Add to the stack if deeperO.")
            
                    
        
    def build(self):
        raise NotImplementedError("You must implement `build`.")
