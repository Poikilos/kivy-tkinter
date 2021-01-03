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
from kivy.kivytkinter import warn

class ParserVariable:
    '''
    A ParserVariable instance holds information about a value.

    Properties:
    className -- The class of the value, if detected. If the type is
                 None, then className holds a string of the word 'None'.
                 However, if no type is detected, then className
                 actually is None.
    '''

    def __init__(self, s, rvalue):
        self.className = None
        self.value = None
        self.comment = None
        self.isCustomClass = False
        if s is not None:
            s = s.strip()
            if rvalue is not None:
                # This is an lvalue.
                # (if an rvalue is present, self is an lvalue--even if
                # className is 'None', in which case this line starts
                # a class--see rvalue.className below).
                if s.startswith("#"):
                    raise ValueError("A comment can't be an lvalue.")
                self.className = None
                if rvalue.className == 'None':
                    # ^ In KV (or YAML with indented lines following),
                    #   the lvalue is a className when the rvalue is not
                    #   specified.
                    self.className = s
                # else the class is determined automatically by Python
                # according to the rvalue.
                self.value = s
                if Parser.isEnclosed(s, "<"):
                    self.className = s[1:-1]
                    self.isCustomClass = True
            else:
                # It is an rvalue.
                # TODO: allow inline comments
                if s.startswith("#"):
                    s = ""
                    self.comment = s[1:]
                if len(s) == 0:
                    self.value = None
                    self.className = 'None'
                elif Parser.isQuoted(s):
                    self.value = s[1:-1]
                    self.className = 'string'
                elif Parser.isEnclosed(s, '('):
                    v = s[1:-1]
                    try:
                        values = [int(c) for c in v.split(",")]
                    except ValueError:
                        try:
                            values = [float(c) for c in v.split(",")]
                        except:
                            values = v.split(",")
                            warn("A tuple of this type is not"
                                 " implemented, it will have strings:"
                                 " `{}`".format(s))
                    self.value = tuple(values)
                    self.className = 'tuple'
                else:
                    try:
                        self.value = int(s)
                        self.className = "int"
                    except ValueError:
                        try:
                            self.value = float(s)
                            self.className = "float"
                        except ValueError:
                            self.value = s

    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __set__(self, instance, value):
        self.value = value

    # def __delete__(self):
    # del self.value


class ParserStatement:
    def __init__(self, line):
        if len(line) == 0:
            raise ValueError("Refusing to split a blank")
        ci = line.find("#")
        aoi = line.find(":")
        if aoi < 0:
            raise SyntaxError("Missing ':' in \"{}\"".format(line))
        else:
            if ci >= 0:
                if ci < aoi:
                    raise RuntimeError("\"{}\" should be parsed as a"
                                       " comment but the parser failed."
                                       "".format(line))

        # self.lvalue = ParserVariable(None, True)
        # self.rvalue = ParserVariable(None, False)
        self.rvalue = ParserVariable(line[aoi+1:].strip(), None)

        self.lvalue = ParserVariable(line[:aoi].strip(), self.rvalue)

        if self.lvalue.value.startswith("<"):
            if not self.lvalue.value.endswith(">"):
                raise ValueError("Missing '>' in {}".format(line))
            # ParserVariable already set className.


class Parser:
    OPENERS = {
        '<': '>',
        '(': ')',
        '{': '}',
        '[': ']',
    }

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
    def isEnclosed(haystack, needle):
        '''
        Sequential arguments:
        needle -- The start and end of the string.
                  If this is a key in Parser.OPENERS, then check the end
                  for Parser.OPENERS[needle] instead of needle.
        '''
        sw = needle
        ew = Parser.OPENERS.get(needle, needle)
        hs = haystack
        return (len(hs) >= 2) and (hs[0] == sw) and (hs[-1] == ew)

    @staticmethod
    def isQuoted(haystack):
        hs = haystack
        return Parser.isEnclosed(hs, "'") or Parser.isEnclosed(hs, '"')

    @staticmethod
    def parserStatement(line):
        return ParserStatement(line)

