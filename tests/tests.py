#!/usr/bin/env python

import os
import sys
from inspect import getmembers, isfunction

if os.path.isfile("../kivy/properties.py"):
    sys.path.append("..")

from kivy.properties import (ListProperty, DictProperty)

d = {
    '0': 'a',
    '1': 'b',
    '3': 'd',
}
d2 = {
    '2': 'c',
}
resultD = {
    '0': 'a',
    '1': 'b',
    '2': 'c',
    '3': 'd',
}
intD = {}

l = ['a', 'b', 'd']
for i in range(len(l)):
    intD[i] = l[i]

resultIntD = {}

resultL = ['a', 'b', 'c', 'd']
for i in range(len(l)):
    resultIntD[i] = resultL[i]


def test_ListProperty_as_list():
    print()
    print("Test ListProperty as list.")
    lp = ListProperty(l.copy())
    sys.stdout.write("{} becomes ".format(lp))
    lp.insert(2, 'c')
    print("{}".format(lp))
    assert lp._l == resultL


def test_ListProperty_as_list_then_dict():
    print()
    print("Test ListProperty as list then dict.")
    lp = ListProperty(l.copy())
    print("BEFORE: {}".format(lp))
    lp.insert('2', 'c')
    print("AFTER: {}".format(lp))
    assert lp._l == resultL


def test_ListProperty_as_dict_then_list():
    print()
    print("Test ListProperty as list then dict.")
    lp = ListProperty(intD.copy())
    print("BEFORE: {}".format(lp))
    lp.insert('2', 'c')
    print("AFTER: {}".format(lp))
    assert lp._d == {0: 'a', 1: 'b', 2: 'd', '2': 'c'}
    # ^ ok since order doesn't matter
    # (It won't have the same indices as resultIntD since resultIntD's
    # indices are all ints--What is more important is that if lp was
    # initialized as a dict, then lp should not convert the indices to
    # ints.)


def test_ListProperty_as_dict():
    '''
    This test exists since children is a ListProperty in kivy but a
    dict in Tkinter.
    '''
    print()
    print("Test ListProperty as dict ({}):"
          "".format(test_ListProperty_as_dict.__doc__.strip()))
    lp = ListProperty(intD.copy())
    sys.stdout.write("{} becomes ".format(lp))
    lp.insert(2, 'c')
    print("{}".format(lp))
    assert lp._d == {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
    # ^ ok since order doesn't matter
    # (It won't have the same indices as resultD)
    # - but indices should be converted to ints since whoever created
    # the list expects that. That would break things in Tkinter but the
    # list is manually recreated as a dict to avoid this behavior (All
    # subclasses of Tkinter widgets should ensure that
    # ListProperty(self.children) is called AFTER calling super in init,
    # since Tkinter remakes children as a dict).


def test_DictProperty_keys_and_values():
    dp = DictProperty(resultD.copy())
    print()
    print("test_DictProperty_keys_and_values:")
    print("  keys:")
    for k in dp.keys():
        print("    - {}".format(k))
    print("  values:")
    for v in dp.values():
        print("    - {}".format(k, v))
    zip1 =  dict(zip(dp.keys(), dp.values()))
    assert zip1 == resultD

def test_DictPropertyIterator():
    dp = DictProperty(resultD.copy())
    print()
    print("test_DictPropertyIterator:")
    print("  pairs:")
    keys = []
    values = []
    for k,v in dp.items():
        keys.append(k)
        values.append(v)
        print("    {}: {}".format(k, v))
    zip2 =  dict(zip(keys, values))
    assert zip2 == resultD



def main():
    mod = sys.modules[__name__]
    for fn in [o for o in getmembers(mod) if isfunction(o[1])]:
        if fn[0].startswith("test_"):
            fn[1]()


if __name__ == "__main__":
    main()
