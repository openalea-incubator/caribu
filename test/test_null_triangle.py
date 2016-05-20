from math import isnan, sqrt
from nose.tools import assert_almost_equal

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_incident_energy_when_no_occlusion_two_triangles():
    pts1 = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    pts2 = [(10, 10, 0), (10 - sqrt(2), 10, 0), (10, 10, 0)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # vertical light
    lights = [(100, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    res = res['band0']['data']

    assert_almost_equal(res['area'][0], 1, 3)
    assert_almost_equal(res['Ei_sup'][0], 100, 0)
    assert_almost_equal(res['Ei_inf'][0], 0, 3)

    assert_almost_equal(res['area'][1], 0, 3)
    assert isnan(res['Ei_sup'][1])
    assert isnan(res['Ei_inf'][1])
