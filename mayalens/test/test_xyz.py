import unittest
from nose.plugins.attrib import attr

from hypothesis import given
import hypothesis.strategies as st

# try:
#     import maya.cmds as cmds
# except ImportError:
#     print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from ..xyz import *

# must be explicit with names with leading underscores
from ..xyz import _x_get, _x_set, _x
from ..xyz import _y_get, _y_set, _y
from ..xyz import _z_get, _z_set, _z


# PURE

class Test_xyz (unittest.TestCase):

    def test__x_get (self):
        self.assertEquals(_x_get((4, 5, 6)), 4)

    def test__x_set (self):
        self.assertEquals(_x_set(1)((4, 6, 8)), (1, 6, 8))

    def test__x_lens_get (self):
        self.assertEquals(_x.get((8, 7, 5)), 8)

    def test__x_lens_set (self):
        self.assertEquals(_x.set(3)((8, 7, 5)), (3, 7, 5))

    def test__x_lens_modify (self):
        self.assertEquals(_x.modify(lambda x: x + 3)((8, 7, 5)), (11, 7, 5))


    def test__y_get (self):
        self.assertEquals(_y_get((4, 5, 6)), 5)

    def test__y_set (self):
        self.assertEquals(_y_set(2)((4, 6, 8)), (4, 2, 8))

    def test__y_lens_get (self):
        self.assertEquals(_y.get((2, 3, 1)), 3)

    def test__y_lens_set (self):
        self.assertEquals(_y.set(2)((2, 3, 1)), (2, 2, 1))

    def test__y_lens_modify (self):
        self.assertEquals(_y.modify(lambda y: y + 4)((2, 3, 1)), (2, 7, 1))


    def test__z_get (self):
        self.assertEquals(_z_get((4, 6, 7)), 7)

    def test__z_set (self):
        self.assertEquals(_z_set(3)((4, 6, 8)), (4, 6, 3))

    def test__z_lens_get (self):
        self.assertEquals(_z.get((7, 9, 0)), 0)

    def test__z_lens_set (self):
        self.assertEquals(_z.set(7)((7, 9, 0)), (7, 9, 7))

    def test__z_lens_modify (self):
        self.assertEquals(_z.modify(lambda z: z + 2)((7, 9, 0)), (7, 9, 2))


# IMPURE

@attr("maya")
class Test_worldLocalObjectGettersSettersLenses (unittest.TestCase):

    def setUp (self):
        cmds.file(new=True, force=True)
        self.loc1 = cmds.spaceLocator()[0]
        self.loc2 = cmds.spaceLocator()[0]
        self.loc3 = cmds.spaceLocator()[0]
        cmds.parent(self.loc3, self.loc2)
        cmds.parent(self.loc2, self.loc1)

        # done backwards as move defaults to ws
        cmds.move(4, -2, -1, self.loc3)
        cmds.move(-1, 5, 7, self.loc2)
        cmds.move(2, 3, 4, self.loc1)

    def test_wsGet (self):
        self.assertEquals(wsGet(self.loc3), (5, 6, 10))

    def test_lsGet (self):
        self.assertEquals(lsGet(self.loc3), (4, -2, -1))

    def test_osGet (self):
        self.assertEquals(osGet(self.loc3), (4, -2, -1))


    def test_wsSet (self):
        wsSet((5, 6, 7))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (5, 6, 7))

    def test_lsSet (self):
        lsSet((1, 2, 3))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (1, 2, 3))

    def test_osSet (self):
        osSet((1, 2, 3))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (1, 2, 3))


    def test_lens_wsXYZ_get (self):
        self.assertEquals(wsXYZ.get(self.loc3), (5, 6, 10))

    def test_lens_wsXYZ_set (self):
        wsXYZ.set((2, 9, 6))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (2, 9, 6))

    def test_lens_wsXYZ_modify (self):
        wsXYZ.modify(lambda (x, y, z): (z, x, y))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (10, 5, 6))


    def test_lens_lsXYZ_get (self):
        self.assertEquals(lsXYZ.get(self.loc3), (4, -2, -1))

    def test_lens_lsXYZ_set (self):
        lsXYZ.set((2, 9, 6))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (2, 9, 6))

    def test_lens_lsXYZ_modify (self):
        lsXYZ.modify(lambda (x, y, z): (z, x, y))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (-1, 4, -2))


    def test_lens_osXYZ_get (self):
        self.assertEquals(osXYZ.get(self.loc3), (4, -2, -1))

    def test_lens_osXYZ_set (self):
        osXYZ.set((2, 9, 6))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (2, 9, 6))

    def test_lens_osXYZ_modify (self):
        osXYZ.modify(lambda (x, y, z): (z, x, y))(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (-1, 4, -2))


    def test_lens_wsX_get (self):
        self.assertEquals(wsX.get(self.loc3), 5)

    def test_lens_wsX_set (self):
        wsX.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (1, 6, 10))

    def test_lens_wsX_modify (self):
        wsX.modify(lambda x: x + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (12, 6, 10))


    def test_lens_lsX_get (self):
        self.assertEquals(lsX.get(self.loc3), 4)

    def test_lens_lsX_set (self):
        lsX.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (1, -2, -1))

    def test_lens_lsX_modify (self):
        lsX.modify(lambda x: x + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (11, -2, -1))


    def test_lens_osX_get (self):
        self.assertEquals(osX.get(self.loc3), 4)

    def test_lens_osX_set (self):
        osX.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (1, -2, -1))

    def test_lens_osX_modify (self):
        osX.modify(lambda x: x + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (11, -2, -1))


    def test_lens_wsY_get (self):
        self.assertEquals(wsY.get(self.loc3), 6)

    def test_lens_wsY_set (self):
        wsY.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (5, 1, 10))

    def test_lens_wsY_modify (self):
        wsY.modify(lambda y: y + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (5, 13, 10))


    def test_lens_lsY_get (self):
        self.assertEquals(lsY.get(self.loc3), -2)

    def test_lens_lsY_set (self):
        lsY.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (4, 1, -1))

    def test_lens_lsY_modify (self):
        lsY.modify(lambda y: y + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (4, 5, -1))


    def test_lens_osY_get (self):
        self.assertEquals(osY.get(self.loc3), -2)

    def test_lens_osY_set (self):
        osY.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (4, 1, -1))

    def test_lens_osY_modify (self):
        osY.modify(lambda y: y + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (4, 5, -1))


    def test_lens_wsZ_get (self):
        self.assertEquals(wsZ.get(self.loc3), 10)

    def test_lens_wsZ_set (self):
        wsZ.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (5, 6, 1))

    def test_lens_wsZ_modify (self):
        wsZ.modify(lambda z: z + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, worldSpace=True, translation=True))
        self.assertEquals(xyz, (5, 6, 17))


    def test_lens_lsZ_get (self):
        self.assertEquals(lsZ.get(self.loc3), -1)

    def test_lens_lsZ_set (self):
        lsZ.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (4, -2, 1))

    def test_lens_lsZ_modify (self):
        lsZ.modify(lambda z: z + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, translation=True))
        self.assertEquals(xyz, (4, -2, 6))


    def test_lens_osZ_get (self):
        self.assertEquals(osZ.get(self.loc3), -1)

    def test_lens_osZ_set (self):
        osZ.set(1)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (4, -2, 1))

    def test_lens_osZ_modify (self):
        osZ.modify(lambda z: z + 7)(self.loc3)
        xyz = tuple(cmds.xform(self.loc3, query=True, objectSpace=True, translation=True))
        self.assertEquals(xyz, (4, -2, 6))

