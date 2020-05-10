try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from lens import Lens, ImpureLens


# PURE

_x_get = lambda (x, _, __): x
_x_set = lambda v: lambda (x, y, z): (v, y, z)
_x = Lens(_x_get, _x_set)

_y_get = lambda (_, y, __): y
_y_set = lambda v: lambda (x, y, z): (x, v, z)
_y = Lens(_y_get, _y_set)

_z_get = lambda (_, __, z): z
_z_set = lambda v: lambda (x, y, z): (x, y, v)
_z = Lens(_z_get, _z_set)


# IMPURE

wsGet = lambda tf: tuple(cmds.xform(tf, query=True, worldSpace=True, translation=True))
wsSet = lambda xyz: lambda tf: cmds.xform(tf, worldSpace=True, translation=xyz)

lsGet = lambda tf: tuple(cmds.xform(tf, query=True, translation=True))
lsSet = lambda xyz: lambda tf: cmds.xform(tf, translation=xyz)

osGet = lambda tf: tuple(cmds.xform(tf, query=True, objectSpace=True, translation=True))
osSet = lambda xyz: lambda tf: cmds.xform(tf, objectSpace=True, translation=xyz)

wsXYZ = ImpureLens(wsGet, wsSet)
lsXYZ = ImpureLens(lsGet, lsSet)
osXYZ = ImpureLens(osGet, osSet)

wsX = wsXYZ | _x
wsY = wsXYZ | _y
wsZ = wsXYZ | _z

lsX = lsXYZ | _x
lsY = lsXYZ | _y
lsZ = lsXYZ | _z

osX = osXYZ | _x
osY = osXYZ | _y
osZ = osXYZ | _z

