from math import sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_incident_energy_when_no_occlusion_single_triangle():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    mats = [green_leaf_PAR]

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)


def test_incident_energy_when_no_occlusion_two_triangles():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(10, 10, 0), (10 - sqrt(2), 10, 0), (10, 10 - sqrt(2), 0)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Ei_sup'][i], 100, 0)
        assert_almost_equal(res['Ei_inf'][i], 0, 3)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Ei_sup'][i], 0, 0)
        assert_almost_equal(res['Ei_inf'][i], 0, 3)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Ei_sup'][i], 100, 0)
        assert_almost_equal(res['Ei_inf'][i], 0, 3)


def test_incident_energy_when_full_occlusion_two_shapes():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(0, 0, 1), (sqrt(2), 0, 1), (0, sqrt(2), 1)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 1, 3)
    assert_almost_equal(res['Ei_sup'][1], 100, 0)
    assert_almost_equal(res['Ei_inf'][1], 0, 3)
