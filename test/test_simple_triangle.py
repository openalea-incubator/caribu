from math import sqrt

from alinea.caribu.caribu import green_leaf_PAR, raycasting


def test_incident_energy_when_no_occlusion_single_triangle():
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = [points]
    mats = [green_leaf_PAR]
    lights = [(1, (0, 0, -1))]
    res = raycasting(triangles, mats, lights)
    print res
    assert False
    # assert abs(res['Area'][sid] - 1) < 1e-3
    # assert abs(res['Ei'][sid] - 100) < 1e-1
    # assert abs(res['Einc'][sid] - 100) < 1e-1

