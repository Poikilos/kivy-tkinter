#!/usr/bin/env python
import os
import inspect
import importlib

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

from kivy.lang import Builder
from kivy.lang import Parser
from kivy.kivytkinter import warn
from kivy.kivytkinter import view_traceback

from kivy.kivytkinter import KT
# ^ this must be done from a dumb file that every file imports, because
#   If files that app.py imports import App, a circular import will
#   occur.

# Now import everything so eval works (This is not Kivy-like at all)
# TODO: improve this (do not use eval?)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class App(tk.Tk):
    IS_TKINTER = True
    KT.MIN_W = 400
    KT.MIN_H = 300

    def __init__(self):
        tk.Tk.__init__(self)
        title = type(self).__name__
        if title.endswith("App"):
            title = title[:-3]
        self.title(title)
        self.minsize(KT.MIN_W, KT.MIN_H)
        # ^ Prevent weird tkinter behavior creating a 1px wide window
        #   only as high as the title bar when fill=tk.BOTH, expand=True
        #   and there are no widgets.
        self.id = None

    def run(self):
        self.parser = Parser(content=Builder._loadedStr)
        self._build()
        KT.APP.mainloop()

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
        Construct the app from KV language lines if present. (Doing so
        here and now is likely not a Kivy-like way of doing things).
        '''
        KT.indent = ""
        tabs = []
        prevIndent = None
        stack = []
        # ^ stack.append doesn't occur until the end of this method.
        # print("I am a {}.".format(str(type(self).__name__)))
        frame = inspect.stack()[2]
        cfp = frame[0].f_code.co_filename
        cf = os.path.split(cfp)[1]
        mod = importlib.import_module(os.path.splitext(cf)[0])
        # print("The file with custom widgets is \"{}\".".format(cfp))
        KT.APP = self
        self.frame = self.build()

        # ^ Ok since kivy-tkinter widget constructors always set the
        #   parent to App.ROOT by default--so no matter how the client
        #   code creates the root widget, the parent will be `App.ROOT`.
        if KT.FORM is not None:
            raise RuntimeError("kivy-tkinter built twice!")
        self.frame.pack(fill=tk.BOTH, expand=True)

        #self.frame.grid(row=0, column=0, sticky=tk.NSEW)
        #tk.Grid.rowconfigure(KT.APP, 0, weight=1)
        #tk.Grid.columnconfigure(KT.APP, 0, weight=1)

        KT.FORM = self.frame
        # self.frame.grid()
        self.frame.parent = KT.APP
        # ^ But technically, KT.APP is the root widget's
        #   (KT.APP.frame's) parent
        lineN = 0
        fn = "KV in {}".format(os.path.split(cfp)[1])
        if self.parser.filename is not None:
            fn = self.parser.filename
        for i in range(len(self.parser.sourcecode)):
            lineN += 1
            line = self.parser.sourcecode[i].rstrip()
            lineS = line.strip()
            if lineS.startswith("#"):
                continue
            # if len(stack) == 0:
            if len(lineS) == 0:
                continue
            dent = line[:(len(line)-len(lineS))]
            # print("indent: \"{}\"".format(dent))
            if len(dent) < len(KT.indent):
                while len("".join(tabs)) > len(dent):
                    if stack[-1].parent is None:
                        raise SyntaxError(dent + "Line {} of {} has more"
                                          " than one root widget near `{}`"
                                          "".format(lineN, fn,
                                                    line.strip()))
                    if stack[-1].parent is not None:
                        pass
                        # add the widget AFTER setting all properties ?
                        # stack[-1].parent.add_widget(stack[-1])
                    del stack[-1]
                    del tabs[-1]
                    '''
                    print(dent + "Line {} of {} starts a new object"
                          " near `{}`.".format(lineN, fn, line.strip()))
                    '''
                if len("".join(tabs)) != len(dent):
                    raise SyntaxError(dent + "Line {} of {} doesn't"
                          " match a previous indent near `{}`."
                          " thisTabSize={}, dent='{}', tabs={}"
                          "".format(lineN, fn, line.strip(),
                                    thisTabSize, dent, tabs))
            KT.indent = dent
            kvc = Parser.parserStatement(lineS)
            deeperO = None
            ThisClass = None
            # thisId = None
            # thisOr = None
            # methodName = None
            if kvc.lvalue.isCustomClass is True:
                try:
                    ThisClass = getattr(mod, kvc.lvalue.className)
                except AttributeError as ex:
                    view_traceback()
                    raise SyntaxError(dent + "Line {} of {} has a"
                                      " custom type not defined in {}"
                                      " near `{}`"
                                      "".format(lineN, fn, cf,
                                                line.strip()))
                # deeperO = ThisClass()
                # print("Creating a new (custom) {}"
                # #   "".format(ThisClass.__name__))
            elif kvc.rvalue.value is None:
                # Syntax "ThisClass:" denotes class (could be null or
                # object declaration in YAML, but is an object
                # declaration in kv)
                try:
                    ThisClass = eval(kvc.lvalue.value)
                except AttributeError as ex:
                    raise SyntaxError(dent + "Line {} of {} has a"
                                      " Kivy type not defined in"
                                      " kivy-tkinter near `{}`"
                                      "".format(lineN, fn,
                                                line.strip()))
                # deeperO = ThisClass()
                # print("Creating a new {}"
                # #     "".format(ThisClass.__name__))
            else:
                if len(stack) == 0:
                    raise SyntaxError(dent + "Line {} of {} has a"
                                      " member before an object near"
                                      " `{}`".format(lineN, fn,
                                                     line.strip()))

                # Add events and properties for both KV and custom
                # classes (regardless of kvc.rvalue.className presence):
                if kvc.lvalue.value == "orientation":
                    stack[-1].orientation = kvc.rvalue.value
                    '''
                    print("[kivy-tkinter kivy app] set {} {}"
                          " orientation to {}"
                          "".format(type(stack[-1]).__name__,
                                    stack[-1].id, kvc.rvalue.value))
                    '''
                elif kvc.lvalue.value == 'id':
                    # thisId = kvc.rvalue.value
                    stack[-1].id = kvc.rvalue.value
                    self.frame.ids[kvc.rvalue.value] = stack[-1]
                elif kvc.lvalue.value == 'text':
                    # thisId = kvc.rvalue.value

                    if callable(stack[-1].text):
                        raise RuntimeError(
                            "The text override failed due to a"
                            " programming error in kivy-tkinter"
                            " itself."
                        )
                        # stack[-1].text(kvc.rvalue.value)
                    stack[-1].text = kvc.rvalue.value
                elif kvc.rvalue.methodName is not None:
                    methodName = kvc.rvalue.methodName
                    if methodName.startswith("root."):
                        methodName = methodName.replace(
                            "root.",
                            "self.frame."
                        )
                        '''
                        print(dent + "using method `{}`"
                              "".format(methodName))
                        '''
                    elif methodName.startswith("self."):
                        methodName = methodName.replace(
                            "self.",
                            "self.frame.ids." + stack[-1].id + "."
                        )
                        '''
                        print(dent + "using method `{}`"
                              "".format(methodName))
                        '''
                    elif methodName.startswith("app."):
                        methodName = methodName.replace(
                            "app.",
                            "KT.APP."
                        )
                        '''
                        print(dent + "using method `{}`"
                              "".format(methodName))
                        '''
                    else:
                        raise NotImplementedError(
                            "The object in  the method call is not"
                            " implemented: {}".format(methodName)
                        )
                    '''
                    print(dent + "trying to add {} to {}"
                          "".format(kvc.lvalue.value,
                                    type(stack[-1]).__name__))
                    '''
                    if kvc.lvalue.value == 'on_press':
                        stack[-1].bind(on_press=eval(methodName))
                    else:
                        raise NotImplementedError(
                            "The `{}` handler is not implemented."
                            "".format(kvc.lvalue.value)
                        )

                elif kvc.rvalue.className is not None:
                    if not hasattr(stack[-1], kvc.lvalue.value):
                        warn(dent + "Line {} of {} has a KV value `{}`"
                             " for {}, which is not implemented, near"
                             " `{}`".format(lineN, fn, kvc.rvalue,
                                            kvc.lvalue, line.strip()))
                    stack[-1].__dict__[kvc.lvalue] = kvc.rvalue.value
                else:
                    # A literal None implies that the parser could not
                    # detect the type.
                    if not hasattr(stack[-1], kvc.lvalue.value):
                        warn(dent + "Line {} of {} has an rvalue"
                             " that will be taken literally: `{}` near"
                             " `{}`".format(lineN, fn, kvc.rvalue,
                                            line.strip()))
                    stack[-1].__dict__[kvc.lvalue] = kvc.rvalue.value
                    # TODO: implement KV rules such as:
                    # right: self.parent.right
                    # right: layout.right # where id of parent is layout

            if ThisClass is not None:
                if len(stack) == 0:
                    deeperO = self.frame
                    # ^ Make the child objects get appended to the frame
                    #   (root widget)
                else:
                    '''
                    if thisOr is not None:
                        deeperO = ThisClass(
                            tkinterParent=stack[-1],
                            orientation=thisOr,
                        )
                    else:
                    '''
                    deeperO = ThisClass(
                        tkinterParent=stack[-1]
                    )
                    '''
                    print(dent + "tkinterParent is {}"
                          "".format(stack[-1]))
                    '''

                    '''
                    msgFmt = (dent + "adding {}"
                              " to {} {} with orientation {}.")
                    print(
                        msgFmt.format(
                            kvc.lvalue.value,
                            type(stack[-1]).__name__,
                            stack[-1].id,
                            stack[-1].orientation,
                        )
                    )
                    '''

                    if not hasattr(stack[-1], 'add_widget'):
                        exFmt = (dent + "Line {} of {} has a `{}`"
                                 " inside of a `{}` near `{}`.")

                        raise SyntaxError(
                            exFmt.format(lineN, fn, kvc.lvalue.value,
                                         type(stack[-1]).__name__,
                                         line.strip())
                        )
                    stack[-1].add_widget(deeperO)
                # if thisId is not None:
                # self.frame.ids[thisId] = deeperO
                stack.append(deeperO)
            thisTabSize = len(dent) - len("".join(tabs))
            '''
            if thisTabSize < 1:
                exFmt = (dent + "[kivy-tkinter app] failed to"
                         " correctly add to the indent on line {} "
                         " of {} near `{}`. This is a failure in"
                         " kivy-tkinter itself. thisTabSize={},"
                         " dent='{}', tabs={}")

                raise RuntimeError(
                    exFmt.format(lineN, fn, line.strip(),
                                 thisTabSize, dent, tabs)
                )
            '''
            if thisTabSize > 0:
                tabs.append(dent[-thisTabSize:])

    def build(self):
        raise NotImplementedError("You must implement `build` and"
                                  " return a root widget.")
