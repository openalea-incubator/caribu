from math import sqrt
from vplants.plantgl.scenegraph import TriangleSet, Scene, Shape

from alinea.caribu.caribu_star import emission_inv, run_caribu
from alinea.caribu.lightString import lightString


def test_incident_energy_when_no_occlusion_single_triangle():
    sid = 10
    # create triangle
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)]
    triangles = TriangleSet(points, [(0, 1, 2)], [(0, 0, 1)],
                            normalPerVertex=False)
    shp = Shape(triangles)
    shp.id = sid
    scene = Scene([shp])

    sources = lightString(emission_inv(90, 100), 0, 0)  # "100 0 0 -1"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 1) < 1e-3
    assert abs(res['Ei'][sid] - 100) < 1e-1
    assert abs(res['Einc'][sid] - 100) < 1e-1

    sources = lightString(emission_inv(0, 100), 90, 0)  # "100 1 0 0"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 1) < 1e-3
    assert abs(res['Ei'][sid]) < 1e-1
    assert abs(res['Einc'][sid]) < 1e-1

    sources = lightString(emission_inv(45, 100), 45, 0)  # "100 1 0 0"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 1) < 1e-3
    assert abs(res['Ei'][sid] - 50 * sqrt(2)) < 1e-1
    assert abs(res['Einc'][sid] - 50 * sqrt(2)) < 1e-1


def test_incident_energy_when_no_occlusion_two_triangles():
    sid = 10
    # create triangle
    points = [(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0),
              (10, 10, 0), (10 - sqrt(2), 10, 0), (10, 10 - sqrt(2), 0)]
    triangles = TriangleSet(points,
                            [(0, 1, 2), (3, 4, 5)],
                            [(0, 0, 1), (0, 0, 1)],
                            normalPerVertex=False)
    shp = Shape(triangles)
    shp.id = sid
    scene = Scene([shp])

    sources = lightString(emission_inv(90, 100), 0, 0)  # "100 0 0 -1"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 2) < 1e-3
    assert abs(res['Ei'][sid] - 100) < 1e-1
    assert abs(res['Einc'][sid] - 200) < 1e-1

    sources = lightString(emission_inv(0, 100), 90, 0)  # "100 1 0 0"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 2) < 1e-3
    assert abs(res['Ei'][sid]) < 1e-1
    assert abs(res['Einc'][sid]) < 1e-1

    sources = lightString(emission_inv(45, 100), 45, 0)  # "100 1 0 0"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 2) < 1e-3
    assert abs(res['Ei'][sid] - 50 * sqrt(2)) < 1e-1
    assert abs(res['Einc'][sid] - 2 * 50 * sqrt(2)) < 1e-1


def test_incident_energy_when_full_occlusion_two_shapes():
    sid1 = 10
    sid2 = 11
    shp1 = Shape(TriangleSet([(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0)],
                             [(0, 1, 2)],
                             [(0, 0, 1)],
                             normalPerVertex=False))
    shp1.id = sid1
    shp2 = Shape(TriangleSet([(0, 0, 1), (sqrt(2), 0, 1), (0, sqrt(2), 1)],
                             [(0, 1, 2)],
                             [(0, 0, 1)],
                             normalPerVertex=False))
    shp2.id = sid2
    scene = Scene([shp1, shp2])

    sources = lightString(emission_inv(90, 100), 0, 0)  # "100 0 0 -1"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid1] - 1) < 1e-3
    assert abs(res['Area'][sid2] - 1) < 1e-3
    assert abs(res['Ei'][sid1] - 0) < 1e-1
    assert abs(res['Ei'][sid2] - 100) < 1e-1
    assert abs(res['Einc'][sid1] - 0) < 1e-1
    assert abs(res['Einc'][sid2] - 100) < 1e-1


def test_incident_energy_when_full_occlusion_two_triangles_single_shape():
    sid = 10
    shp = Shape(TriangleSet([(0, 0, 0), (sqrt(2), 0, 0), (0, sqrt(2), 0),
                             (0, 0, 10), (sqrt(2), 0, 10), (0, sqrt(2), 10)],
                            [(0, 1, 2), (3, 4, 5)],
                            [(0, 0, 1), (0, 0, 1)],
                            normalPerVertex=False))
    shp.id = sid
    scene = Scene([shp])

    sources = lightString(emission_inv(90, 100), 0, 0)  # "100 0 0 -1"
    res = run_caribu(sources, scene, opticals='leaf')
    assert abs(res['Area'][sid] - 2) < 1e-3
    assert abs(res['Ei'][sid] - 50) < 1e-1
    assert abs(res['Einc'][sid] - 100) < 1e-1


