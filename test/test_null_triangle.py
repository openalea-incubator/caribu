from math import isnan, sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_null_triangle1():
    pts1 = [(0, 0, 0), (1, 0, 0), (1, 0, 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]
    lights = [(100, (0, 0, -1))]

    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 0, 3)
    assert isnan(res['Ei_sup'][0])
    assert isnan(res['Ei_inf'][0])


def test_null_triangle2():
    pts1 = [(0, 0, 0), (1, 0, 0), (0.5, 0, 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]
    lights = [(100, (0, 0, -1))]

    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 0, 3)
    assert isnan(res['Ei_sup'][0])
    assert isnan(res['Ei_inf'][0])


def test_incident_energy_when_no_occlusion_two_triangles():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(10, 10, 0), (10 - sqrt(2), 10, 0), (10, 10, 0)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0, 3)
    assert isnan(res['Ei_sup'][1])
    assert isnan(res['Ei_inf'][1])


def test_null_triangle_inside_domain():
    pts1 = [(0, 1, 0), (0, 0, 0), (1, 0, 0)]
    pts2 = [(0, 1, 0), (1, 0, 0), (1, 0, 0)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2
    lights = [(100, (0, 0, -1))]

    domain = (-2, -2, 2, 2)
    res = raycasting(triangles, mats, lights, domain)
    print res

    assert_almost_equal(res['area'][0], 0.5, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0, 3)
    assert isnan(res['Ei_sup'][1])
    assert isnan(res['Ei_inf'][1])


def test_null_triangle_outside_domain():
    pts1 = [(0, 1, 0), (0, 0, 0), (1, 0, 0)]
    pts2 = [(2, 1, 0), (3, 0, 0), (3, 0, 0)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2
    lights = [(100, (0, 0, -1))]

    domain = (-2, -2, 2, 2)
    res = raycasting(triangles, mats, lights, domain)

    assert_almost_equal(res['area'][0], 0.5, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0, 3)
    assert isnan(res['Ei_sup'][1])
    assert isnan(res['Ei_inf'][1])
