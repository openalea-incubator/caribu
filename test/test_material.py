from math import isnan, sqrt
from nose.tools import assert_almost_equal, assert_raises

from alinea.caribu.caribu import (green_leaf_PAR, mixed_radiosity, radiosity,
                                  raycasting)


# def test_raycasting_opaque():
#     points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
#     triangles = [points]
#     lights = [(100, (0, 0, -1))]
#
#     # no reflectance, black body
#     materials = [(0., )]
#     res = raycasting(triangles, materials, lights)
#     assert_almost_equal(res['area'][0], 1, 3)
#     assert_almost_equal(res['Ei_sup'][0], -1, 3)
#     assert_almost_equal(res['Ei_inf'][0], -1, 3)
#     # assert_almost_equal(res['Eabs'][0], 100, 3)
#
#     # full reflectance, mirror
#     materials = [(1., )]
#     res = raycasting(triangles, materials, lights)
#     assert_almost_equal(res['area'][0], 1, 3)
#     assert_almost_equal(res['Ei_sup'][0], -1, 0)
#     assert_almost_equal(res['Ei_inf'][0], -1, 3)
#     # assert_almost_equal(res['Eabs'][0], 0, 3)
#
#     # semi reflectance
#     materials = [(0.1, )]
#     res = raycasting(triangles, materials, lights)
#     assert_almost_equal(res['area'][0], 1, 3)
#     assert_almost_equal(res['Ei_sup'][0], -1, 0)
#     assert_almost_equal(res['Ei_inf'][0], -1, 3)
#     assert_almost_equal(res['Eabs'][0], 90, 3)


def test_raycasting_translucent():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    lights = [(100, (0, 0, -1))]

    # no reflectance, black body
    materials = [(0., 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], -1, 3)
    assert_almost_equal(res['Ei_inf'][0], -1, 3)
    assert isnan(res['Eabs'][0])

    # full reflectance, mirror
    materials = [(1., 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 0, 3)

    # semi reflectance
    materials = [(0.1, 0.)]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
    assert_almost_equal(res['Eabs'][0], 90, 0)

