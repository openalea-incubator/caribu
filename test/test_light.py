from math import sqrt, radians, cos
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_vertical_light():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]

    # vertical light no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)

    # vertical light full intensity
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 100, 0)

    # vertical light full intensity, vertical triangle
    pts1 = [(0, 0, 0), (0, sqrt(2), 0), (0, 0, sqrt(2))]
    triangles = [pts1]
    lights = [(100, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)


def test_horizontal_light():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]

    # horizontal light no intensity
    lights = [(0, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)

    # horizontal light full intensity
    lights = [(100, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)

    # horizontal light full intensity, infinite canopy
    lights = [(100, (-1, 0, 0))]
    domain = (-2, -2, 2, 2)
    res = raycasting(triangles, mats, lights, domain)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)

    # horizontal light full intensity, vertical triangle (impossible case)
    pts1 = [(0, 0, 0), (0, sqrt(2), 0), (0, 0, sqrt(2))]
    triangles = [pts1]
    lights = [(100, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 0, 0)


def test_diagonal_light():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [pts1]
    materials = [green_leaf_PAR]

    # full intensity on horizontal surface
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 100, 0)

    # full intensity perpendicular to the source
    emission = 100
    apparent_emission = emission * cos(radians(45))
    lights = [(apparent_emission, (-1, 0, -1))]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei'][0], 100 * cos(radians(45)), 0)

    # full intensity perpendicular to the source, inclined triangle
    emission = 100
    apparent_emission = emission * cos(radians(45))
    lights = [(apparent_emission, (-1, 0, -1))]
    proj = cos(radians(45))
    pts1 = [(0, 0, 0), (0, sqrt(2), 0), (-sqrt(2) * proj, 0, proj * sqrt(2))]
    triangles = [pts1]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 0)
    assert_almost_equal(res['Ei'][0], 100, 0)

    # full intensity on horizontal surface, inclined triangle
    lights = [(100, (-1, 0, -1))]
    proj = cos(radians(45))
    pts1 = [(0, 0, 0), (0, sqrt(2), 0), (-sqrt(2) * proj, 0, proj * sqrt(2))]
    triangles = [pts1]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 0)
    assert_almost_equal(res['Ei'][0], 141, 0)