from collections import namedtuple


Vector2 = namedtuple("Vector", ["x", "y"])
Vector3 = namedtuple("Vector", ["x", "y", "z"])


def Vector(x, y, z=None):
    if not z: return Vector2(x, y)
    else: return Vector3(x, y, z)


def VectorMult(v, n):
    return Vector(*[ k*n for k in v ])


def VectorNormalize(v):
    vl = sum([k*k for k in v])**(1/2)
    return Vector(*[k/vl for k in v])


def VectorDot(v1, v2):
    assert len(v1) == len(v2)
    return sum([ a*b for a, b in zip(v1, v2) ])