from math import sqrt
from nose.tools import assert_almost_equal, assert_raises

from alinea.caribu.caribu import (green_leaf_PAR, mixed_radiosity, radiosity,
                                  raycasting)


def test_raycasting_single_triangle():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    materials = [(0.06, 0.04)]

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Eabs'][0], 90, 0)
    assert_almost_equal(res['Ei'][0], 100, 0)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Eabs'][0], 0, 0)
    assert_almost_equal(res['Ei'][0], 0, 0)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, materials, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Eabs'][0], 90, 0)
    assert_almost_equal(res['Ei'][0], 100, 0)


def test_raycasting_two_triangles_no_occlusion():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(10, 10, 0), (10 - sqrt(2), 10, 0), (10, 10 - sqrt(2), 0)]
    triangles = [pts1, pts2]
    materials = [(0.06, 0.04)] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, materials, lights)
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Eabs'][i], 90, 0)
        assert_almost_equal(res['Ei'][i], 100, 0)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, materials, lights)
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Eabs'][i], 0, 0)
        assert_almost_equal(res['Ei'][i], 0, 0)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, materials, lights)
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Eabs'][i], 90, 0)
        assert_almost_equal(res['Ei'][i], 100, 0)


def test_raycasting_two_triangles_full_occlusion():
    lower_pts = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    upper_pts = [(0, 0, 1e-5), (sqrt(2), 0, 1e-5), (0, sqrt(2), 1e-5)]
    triangles = [lower_pts, upper_pts]
    lower, upper = 0, 1
    materials = [(0.06, 0.04)] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, materials, lights)

    assert_almost_equal(res['area'][lower], 1, 3)
    assert_almost_equal(res['Eabs'][lower], 0, 0)
    assert_almost_equal(res['Ei'][lower], 0, 0)

    assert_almost_equal(res['area'][upper], 1, 3)
    assert_almost_equal(res['Eabs'][upper], 90, 0)
    assert_almost_equal(res['Ei'][upper], 100, 0)


def test_radiosity_two_triangles_full_occlusion():
    lower_pts = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    upper_pts = [(0, 0, 1e-5), (sqrt(2), 0, 1e-5), (0, sqrt(2), 1e-5)]
    triangles = [lower_pts, upper_pts]
    lower, upper = 0, 1
    materials = [(0.06, 0.04)] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = radiosity(triangles, materials, lights)

    assert_almost_equal(res['area'][lower], 1, 3)
    assert_almost_equal(res['Eabs'][lower], 3.6, 1)
    assert_almost_equal(res['Ei'][lower], 4, 0)

    assert_almost_equal(res['area'][upper], 1, 3)
    assert_almost_equal(res['Eabs'][upper], 90, 0)
    assert_almost_equal(res['Ei'][upper], 100, 0)
    

def test_mixed_radiosity_three_triangles_full_occlusion():
    # mixed radiosity needs at least two triangle
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(0, 0, 0.5), (sqrt(2), 0, 0.5), (0, sqrt(2), 0.5)]
    pts3 = [(0, 0, 1), (sqrt(2), 0, 1), (0, sqrt(2), 1)]
    triangles = [pts1, pts2, pts3]
    materials = [(0.1, )] * 3
    domain = (-2, -2, 2, 2)

    # vertical light
    lights = [(100, (0, 0, -1))]
    diameter, layers, height = 0.6, 3, 1.2
    res = mixed_radiosity(triangles, materials, lights, domain, diameter, layers, height)

    assert_almost_equal(res['area'][0], 1, 3)
    # assert_almost_equal(res['Ei_sup'][0], -1, 0)
    # assert_almost_equal(res['Ei_inf'][0], -1, 3)

    assert_almost_equal(res['area'][2], 1, 3)
    # assert_almost_equal(res['Ei_sup'][2], -1, 0)
    # assert_almost_equal(res['Ei_inf'][2], -1, 3)
    # TODO radiosity result