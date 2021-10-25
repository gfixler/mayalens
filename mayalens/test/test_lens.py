import unittest
from nose.plugins.attrib import attr

from hypothesis import given
import hypothesis.strategies as st

from ..lens import Lens, ImpureLens


ident = lambda x: x
const = lambda x: lambda _: x


class Test_Lens (unittest.TestCase):

    def test_canCreateIdentityLens (self):
        myLens = Lens(ident, const)
        self.assertEquals(myLens.get("foo"), "foo")
        self.assertEquals(myLens.set("bar")("foo"), "bar")
        self.assertEquals(myLens.modify(const("baz"))("foo"), "baz")

    def test_callingLensGetsValue (self):
        myLens = Lens(ident, const)
        expected = myLens.get(const("baz"))("foo")
        actual = myLens(const("baz"))("foo")
        self.assertEquals(expected, actual)

