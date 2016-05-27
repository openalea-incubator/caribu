from nose.tools import assert_raises

from alinea.caribu.caribu import green_leaf_PAR, radiosity, raycasting


def test_default_light_in_raycasting():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [pts1]
    mats = [green_leaf_PAR]

    # default light
    res = raycasting(triangles, mats)

    assert 'area' in res


def test_default_light_in_radiosity():
    pts1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    pts2 = [(0, 0, 1), (1, 0, 1), (0, 1, 1)]
    triangles = [pts1, pts2]
    mats = [green_leaf_PAR] * 2

    # default light
    res = radiosity(triangles, mats)

    assert 'area' in res


def test_raycasting_exception_single_triangle():
    points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [points]

    # black body
    materials = [(0,)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0.,)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0., 0)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))
    materials = [(0., 0, 0, 0.)]
    assert_raises(ValueError, lambda: raycasting(triangles, materials))

    # unmatch
    materials = [(0.1,)] * 2
    assert_raises(ValueError, lambda: raycasting(triangles, materials))


def test_radiosity_exception_single_triangle():
    points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    triangles = [points]
    materials = [green_leaf_PAR]

    # this test should return Value Error
    assert_raises(ValueError, lambda: radiosity(triangles, materials))



