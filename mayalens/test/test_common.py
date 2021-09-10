import unittest
from nose.plugins.attrib import attr

# try:
#     import maya.cmds as cmds
# except ImportError:
#     print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from ..common import *

# must be explicit with names with leading underscores
from ..common import _1_get, _1_set, _1
from ..common import _2_get, _2_set, _2


# PURE

class Test_pairs (unittest.TestCase):

    def test__1_get (self):
        self.assertEquals(_1_get((2, 7)), 2)

    def test__1_set (self):
        self.assertEquals(_1_set(5)((2, 7)), (5, 7))

    def test_lens_1_get (self):
        self.assertEquals(_1.get((1, 5)), 1)

    def test_lens_1_set (self):
        self.assertEquals(_1.set(7)((3, 2)), (7, 2))

    def test_lens_1_modify (self):
        self.assertEquals(_1.modify(lambda a: a * 3)((3, 4)), (9, 4))


    def test__2_get (self):
        self.assertEquals(_2_get((2, 7)), 7)

    def test__2_set (self):
        self.assertEquals(_2_set(5)((2, 7)), (2, 5))

    def test_lens_2_get (self):
        self.assertEquals(_2.get((1, 5)), 5)

    def test_lens_2_set (self):
        self.assertEquals(_2.set(7)((3, 2)), (3, 7))

    def test_lens_2_modify (self):
        self.assertEquals(_2.modify(lambda b: b * 3)((3, 4)), (3, 12))


class Test_lists (unittest.TestCase):

    def test_nth_get (self):
        self.assertEquals(nth(3).get([1, 2, 3, 4, 5]), 4)

    def test_nth_set (self):
        self.assertEquals(nth(2).set(6)([1, 2, 3, 4, 5]), [1, 2, 6, 4, 5])

    def test_lens_nth_get (self):
        self.assertEquals(nth(3).get([7, 1, 4, 2, 5]), 2)

    def test_lens_nth_set (self):
        self.assertEquals(nth(2).set(3)([4, 1, 7, 5]), [4, 1, 3, 5])

    def test_lens_nth_modify (self):
        self.assertEquals(nth(2).modify(lambda n: n * 3)([8, 5, 3, 2]), [8, 5, 9, 2])


class Test_chars (unittest.TestCase):

    def test_charAt_get (self):
        self.assertEquals(charAt_get(2)("testing"), "s")

    def test_charAt_set (self):
        self.assertEquals(charAt_set(2)("mp")("testing"), "tempting")

    def test_lens_charAt_get (self):
        self.assertEquals(charAt(2).get("word"), "r")

    def test_lens_charAt_set (self):
        self.assertEquals(charAt(2).set("t")("how"), "hot")

    def test_lens_charAt_modify (self):
        self.assertEquals(charAt(1).modify(lambda c: "e")("how"), "hew")


class Test_dicts (unittest.TestCase):

    def test_dkey_get (self):
        self.assertEquals(dkey_get("foo")({"bar": 5, "foo": 3}), "foo")

    def test_dkey_set (self):
        self.assertEquals(dkey_set("foo")("quux")({"bar": 5, "foo": 3}), {"bar": 5, "quux": 3})

    def test_lens_dkey_get (self):
        self.assertEquals(dkey("foo").get({"bar": 5, "foo": 3}), "foo")

    def test_lens_dkey_set (self):
        self.assertEquals(dkey("foo").set("quux")({"bar": 5, "foo": 3}), {"bar": 5, "quux": 3})

    def test_lens_dkey_modify (self):
        self.assertEquals(dkey("foo").modify(str.upper)({"bar": 5, "foo": 3}), {"bar": 5, "FOO": 3})


    def test_dval_get (self):
        self.assertEquals(dval_get("foo")({"bar": 5, "foo": 3}), 3)

    def test_dval_set (self):
        self.assertEquals(dval_set("foo")(7)({"bar": 5, "foo": 3}), {"bar": 5, "foo": 7})

    def test_lens_dval_get (self):
        self.assertEquals(dval("foo").get({"bar": 5, "foo": 3}), 3)

    def test_lens_dval_set (self):
        self.assertEquals(dval("foo").set(7)({"bar": 5, "foo": 3}), {"bar": 5, "foo": 7})

    def test_lens_dval_modify (self):
        self.assertEquals(dval("foo").modify(lambda n: n * 3)({"bar": 5, "foo": 3}), {"bar": 5, "foo": 9})

