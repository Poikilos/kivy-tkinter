#!/usr/bin/env python

try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
except ImportError:  # Python 2
    import Tkinter as tk
    import tkFont
    import ttk

from kivy.kivytkinter import warn



class ListPropertyIterator:
    def __init__(self, lp):
        self._lp = lp
        self._index = 0

    def __next__(self):
        if self._index < len(self._lp._l):
            result = self._lp._l[self._index]
            self._index += 1
            return result
        raise StopIteration


class ListProperty:
    '''
    This must act like a dict AND a dict, since children is a
    ListProperty in kivy but a dict in Tkinter.
    '''

    def __init__(self, *args):
        self._silent = False
        self._l = []
        self._d = {}
        self._defaultAs = 'list'
        if len(args) == 1:
            if hasattr(args[0], 'append'):
                self._l = args[0]
                for i in range(len(self._l)):
                    self._d[i] = self._l[i]
            elif hasattr(args[0], 'items'):
                self._d = args[0]
                for k,v in self._d.items():
                    self._l.append(v)
                self._defaultAs = 'dict'
            else:
                raise ValueError("Only a list/dict constructor argument"
                                 " is implemented"
                                 " for {}.".format(type(self).__name__))
        elif len(args) > 1:
            raise ValueError("Only 0-1 arguments are implemented for"
                             " {}.".format(type(self).__name__))

    def __iter__(self):
        return ListPropertyIterator(self)

    def __set__(self, value):
        if hasattr(value, 'keys'):
            self._defaultAs = 'dict'
            self._d = value
            self._l = value.keys()
        else:
            self._l = value
            self._d = {}
            for i in range(len(value)):
                self._d[i] = value[i]

    def __str__(self):
        if self._defaultAs == 'dict':
            return str(self._d)
        return str(self._l)

    def __getitem__(self, key):
        if self._defaultAs == 'dict':
            return self._d[key]
        return self._l[key]

    def __setitem__(self, key, value):
        self._d[key] = value
        try:
            index = int(key)
            if index < len(self._l):
                self._l[key] = value
            elif index == len(self._l):
                if self._defaultAs == 'list':
                    raise IndexError("list assignment index"
                                     " out of range")
            else:
                raise IndexError("list assignment index out of range")
                # ^ Mimic the Python list behavior.
        except ValueError as ex:
            if self._defaultAs == 'list':
                raise ex

    def get(self, key):
        return self._d.get(key)

    def items(self):
        return self._d.items()

    def keys(self):
        return self._d.keys()

    def popitem(self):
        result = self._d.popitem()
        if self._defaultAs == 'list':
            warn("The ListProperty was used as a list but dict-like"
                 " popitem was used (will get '{}')".format(result))
        return result

    def setdefault(self, key, *args):
        default = None
        if len(args) > 0:
            default = args[0]
        self.insert(key, default)

    def update(self, *args):
        if len(args) > 0:
            prevSilent = self._silent
            self._silent = True
            for k,v in args[0].items():
                self.insert(k, v)
            self._silent = prevSilent

    def values(self):
        return self._d.values()

    def append(self, item):
        self._l.append(item)
        self._d[len(self._l)] = item

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def insert(self, i, x):
        try:
            for di in reversed(range(i, len(self._l))):
                self._d[di+1] = self._d[di]
        except TypeError as ex:
            # 'str' object cannot be interpreted as an integer
            warn("A ListProperty was used as a list then a dict.")
        try:
            self._l.insert(i, x)
        except TypeError as ex:
            # 'str' object cannot be interpreted as an integer
            if self._defaultAs == 'list':
                ok = False
                try:
                    index = int(i)
                    self._l.insert(index, x)
                    ok = True
                except ValueError:
                    pass
                if not self._silent:
                    suffix = " (succeeded as int)"
                    if not ok:
                        suffix = " (int() failed)"
                    warn("ListProperty was used as a list but there was"
                         " an attempt to insert at '{}' {}"
                         "".format(i, suffix))
        self._d[i] = x


    def remove(self, item):
        index = None
        try:
            index = self._l.index(item)
            self._l.remove(item)
            del self._d[index]
        except ValueError as ex:
            raise ex

    def pop(self, *args):
        if len(args) == 1:
            result = None
            if self._defaultAs == 'list':
                result = self._l.pop(args[0])
                del self._d[args[0]]
            else:
                result = self._d.pop(args[0])
                try:
                    self._l.pop(args[0])
                except TypeError:
                    # ^ list.pop only accepts an int
                    pass
            return result
        elif len(args) > 1:
            raise ValueError("Only 0-1 arguments are implemented for"
                             " {}.pop.".format(type(self).__name__))
        else:
            result = self._l.pop()
            del self._d[len(self._l)]
            return result

    def index(self, needle, *args):
        start = 1
        end = len(self._l)
        if len(args) > 0:
            start = args[0]
            if len(args) > 1:
                end = args[1]
        for i in range(start, end):
            if self._l[i] == needle:
                return i
        raise ValueError("There is no item {}.".format(needle))

    def clear(self):
        del self._l[:]
        self._d = {}

    def count(self, needle):
        c = 0
        for item in self._l:
            if item == needle:
                c += 1
        return c

    def sort(self, key=None, reverse=False):
        self._l.sort(key=key, reverse=reverse)

    def reverse(self):
        self._l.reverse()

    def copy(self):
        lp = None
        if self._defaultAs == 'dict':
            lp = ListProperty(self._d)
        else:
            lp = ListProperty(self._l)
        return lp


class DictPropertyIterator:
    def __init__(self, dp):
        self._dp = dp
        self._keys = dp.keys()
        self._index = 0

    def __next__(self):
        if self._index < len(self._keys):
            key = self._keys[self._index]
            result = (key, self._dp[key])
            self._index += 1
            return result
        raise StopIteration


class DictProperty(ListProperty):

    def __iter__(self):
        return DictPropertyIterator(self)

'''
    def __init__(self, *args):
        if len(args) == 1:
            for k,v in args[0].items():
                self[k] = v
        elif len(args) > 1:
            raise ValueError("Only 0-1 arguments are implemented for"
                             " {}.".format(type(self).__name__))

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

'''

class NumericProperty:
    def __init__(self, *args):
        raise NotImplementedError


class ObjectProperty:
    def __init__(self, *args):
        raise NotImplementedError


class StringProperty:
    def __init__(self, *args):
        raise NotImplementedError

