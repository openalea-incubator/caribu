from math import sqrt
from nose.tools import assert_almost_equal, assert_raises

from alinea.caribu.caribu import x_radiosity


def test_radiosity_two_triangles_full_occlusion():
    lower_pts = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    upper_pts = [(0, 0, 1e-5), (sqrt(2), 0, 1e-5), (0, sqrt(2), 1e-5)]
    triangles = [lower_pts, upper_pts]
    lower, upper = 0, 1

    # vertical light, opaque material
    lights = [(100, (0, 0, -1))]
    materials = dict(band1=[(0.1, )] * 2,
                     band2=[(0.2, )] * 2)
    x_res = x_radiosity(triangles, materials, lights)

    for band in ("band1", "band2"):
        res = x_res[band]
        assert_almost_equal(res['area'][lower], 1, 3)
        assert_almost_equal(res['Ei_sup'][lower], 0, 0)
        assert_almost_equal(res['Ei_inf'][lower], -1, 3)

        assert_almost_equal(res['area'][upper], 1, 3)
        assert_almost_equal(res['Ei_sup'][upper], 100, 0)
        assert_almost_equal(res['Ei_inf'][upper], -1, 3)
        assert_almost_equal(res['Eabs'][upper], 90, 0)
    #
    # # vertical light, translucent material of upper triangle
    # lights = [(100, (0, 0, -1))]
    # materials = [(0.1, ), (0.1, 0.2)]
    # res = radiosity(triangles, materials, lights)
    #
    # assert_almost_equal(res['area'][lower], 1, 3)
    # assert_almost_equal(res['Ei_sup'][lower], 20, 0)
    # assert_almost_equal(res['Ei_inf'][lower], -1, 3)
    # assert_almost_equal(res['Eabs'][lower], 18, 0)
    #
    # assert_almost_equal(res['area'][upper], 1, 3)
    # assert_almost_equal(res['Ei_sup'][upper], 100, 0)
    # assert_almost_equal(res['Ei_inf'][upper], 1.8, 0)
    # assert_almost_equal(res['Eabs'][upper], 71, 0)
    #
