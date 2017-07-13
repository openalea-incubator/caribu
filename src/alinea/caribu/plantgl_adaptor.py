# -*- python -*-
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       WebSite : https://github.com/openalea-incubator/caribu
#
# ==============================================================================
""" Adaptor for PlantGL object and derived
"""
import numpy
import openalea.plantgl.all as pgl


def _triangle(index, pts):
    return tuple([tuple([x for x in pts[i]]) for i in index])


def pgl_to_triangles(pgl_object, tesselator=None):
    if tesselator is None:
        tesselator = pgl.Tesselator()
    pgl_object.apply(tesselator)
    mesh = tesselator.triangulation
    if mesh:
        pts = numpy.array(mesh.pointList, ndmin=2)
        indices = numpy.array(mesh.indexList, ndmin=2)
        return [_triangle(itri, pts) for itri in indices]
    else:
        return []


def scene_to_cscene(scene):
    """ Build a caribu-compatible scene from a PlantGl scene

    Args:
        scene: an openalea.plantgl.all.Scene instance

    Returns:
        a {primitive_id: [triangles,]} dict.A triangle is a 3-tuple of 3-tuples points coordinates
        primitive_id is taken as the index of the shape in the scene shape list.

    """

    cscene = {}
    tesselator = pgl.Tesselator()
    for pid, pgl_object in enumerate(scene):
        triangles = pgl_to_triangles(pgl_object, tesselator)
        if triangles:
            cscene[pid] = triangles

    return cscene


def mtg_to_cscene(g, property_name='geometry'):
    """Build a caribu-compatible scene from a mtg encoding geometries

    Args:
        g: an openalea.mtg.mtg.MTG instance
        property_name: (str) the name of the property in g where plantGL geometries are encoded

    Returns:
        a {primitive_id: [triangles,]} dict.A triangle is a 3-tuple of 3-tuples points coordinates
        primitive_id is the vertex id.

    """
    geometry = g.property(property_name)
    tesselator = pgl.Tesselator()
    cscene = {}
    for pid in geometry:
        cscene[pid] = pgl_to_triangles(geometry[pid], tesselator)

    return cscene
