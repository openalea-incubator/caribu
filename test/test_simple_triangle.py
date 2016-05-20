from math import sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, radiosity, raycasting, mixed_radiosity


def test_incident_energy_when_no_occlusion_single_triangle():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    mats = [green_leaf_PAR]

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, mats, lights)
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
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Ei_sup'][i], 100, 0)
        assert_almost_equal(res['Ei_inf'][i], 0, 3)

    # vertical light, no intensity
    lights = [(0, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    for i in (0, 1):
        assert_almost_equal(res['area'][i], 1, 3)
        assert_almost_equal(res['Ei_sup'][i], 0, 0)
        assert_almost_equal(res['Ei_inf'][i], 0, 3)

    # diagonal light
    lights = [(100, (-1, 0, -1))]
    res = raycasting(triangles, mats, lights)
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

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 1, 3)
    assert_almost_equal(res['Ei_sup'][1], 100, 0)
    assert_almost_equal(res['Ei_inf'][1], 0, 3)


def test_radiosity_energy_when_no_occlusion_single_triangle():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    mats = [green_leaf_PAR]

    # vertical light
    lights = [(100, (0, 0, -1))]
    # this test should return Value Error
    try:
        res = radiosity(triangles, mats, lights)
        assert False
    except ValueError:
        assert True
        
def test_radiosity_energy_when_full_occlusion_two_shapes():
    # radiosity needs at least two triangle
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(0, 0, 1), (sqrt(2), 0, 1), (0, sqrt(2), 1)]
    triangles = [pts1, pts2]
    mats = [(0.1)] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = radiosity(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], -1, 3)

    assert_almost_equal(res['area'][1], 1, 3)
    assert_almost_equal(res['Ei_sup'][1], 100, 0)
    assert_almost_equal(res['Ei_inf'][1], -1, 3)

def test_mixed_radiosity_energy_when_full_occlusion_three_shapes():
    # radiosity needs at least two triangle
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(0, 0, 0.5), (sqrt(2), 0, 0.5), (0, sqrt(2), 0.5)]
    pts3 = [(0, 0, 1), (sqrt(2), 0, 1), (0, sqrt(2), 1)]
    triangles = [pts1, pts2, pts3]
    mats = [(0.1)] * 3
    domain = (-2, -2, 2, 2)
    
    # vertical light
    lights = [(100, (0, 0, -1))]
    diameter, layers, height = 0.6, 3, 1.2
    res = mixed_radiosity(triangles, mats, lights, domain, diameter, layers, height)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], -1, 3)

    assert_almost_equal(res['area'][2], 1, 3)
    assert_almost_equal(res['Ei_sup'][2], 100, 0)
    assert_almost_equal(res['Ei_inf'][2], -1, 3)

