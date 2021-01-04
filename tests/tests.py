#!/usr/bin/env python

import os
import sys
from inspect import getmembers, isfunction

if os.path.isfile("../kivy/properties.py"):
    sys.path.append("..")

from kivy.properties import ListProperty

d = {
    '0': 'a',
    '1': 'b',
    '3': 'd',
}
d2 = {
    '2': 'c',
}
intD = {}

l = ['a', 'b', 'd']
for i in range(len(l)):
    intD[i] = l[i]


def test_ListProperty_as_list():
    print()
    print("Test ListProperty as list.")
    lp = ListProperty(l.copy())
    sys.stdout.write("{} becomes ".format(lp))
    lp.insert(2, 'c')
    print("{}".format(lp))


def test_ListProperty_as_list_then_dict():
    print()
    print("Test ListProperty as list then dict.")
    lp = ListProperty(l.copy())
    print("BEFORE: {}".format(lp))
    lp.insert('2', 'c')
    print("AFTER: {}".format(lp))


def test_ListProperty_as_dict_then_list():
    print()
    print("Test ListProperty as list then dict.")
    lp = ListProperty(intD.copy())
    print("BEFORE: {}".format(lp))
    lp.insert('2', 'c')
    print("AFTER: {}".format(lp))


def test_ListProperty_as_dict():
    '''
    This test exists since children is a ListProperty in kivy but a
    dict in Tkinter.
    '''
    print()
    print("Test ListProperty as dict ({})".format(test_ListProperty_as_dict.__doc__.strip()))
    lp = ListProperty(intD.copy())
    sys.stdout.write("{} becomes ".format(lp))
    lp.insert(2, 'c')
    print("{}".format(lp))


def main():
    mod = sys.modules[__name__]
    for fn in [o for o in getmembers(mod) if isfunction(o[1])]:
        if fn[0].startswith("test_"):
            fn[1]()


if __name__ == "__main__":
    main()
