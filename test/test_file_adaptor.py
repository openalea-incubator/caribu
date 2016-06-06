"""
Unit test for reader module
"""

from alinea.caribu.file_adaptor import read_light, read_pattern, read_opt, read_can, get_materials
from alinea.caribu.data_samples import data_path


def test_light():
    sky = data_path('zenith.light')
    lights = read_light(sky)
    assert len(lights) == 1
    assert lights[0][0] == 1
    assert lights[0][1] == (0, 0, -1)

    sky = data_path('Turtle16soc.light')
    lights = read_light(sky)
    assert len(lights) == 16

    return lights


def test_pattern():
    path = data_path('filter.8')
    domain = read_pattern(path)
    assert domain == (0, 0, 20, 20)
    return domain


def test_opt():
    path = data_path('par.opt')
    n, s, opts = read_opt(path)

    assert n == 2
    assert s == 0.15
    assert opts[1] == (0.1, 0.1, 0.05, 0.1, 0.05)

    return n, s, opts


def test_can():
    can = data_path('filterT.can')
    labels, triangles = read_can(can)
    assert len(labels) == 192
    assert len(triangles[0]) == 3
    assert len(triangles[0][0]) == 3

    return labels, triangles


def test_materials():
    can = data_path('filterT.can')
    labels, triangles = read_can(can)
    path = data_path('par.opt')
    n, s, opts = read_opt(path)
    materials = get_materials(labels, opts, s)
    assert len(materials) == len(triangles)
    assert materials[0] == (0.1, 0.05)
    return materials
