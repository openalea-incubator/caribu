from math import sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_incident_energy_when_horizontal_direction_light():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]

    # horizontal light no intensity
    lights = [(0, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    # horizontal light no intensity
    lights = [(100, (-1, 0, 0))]
    res = raycasting(triangles, mats, lights)

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 0, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)
