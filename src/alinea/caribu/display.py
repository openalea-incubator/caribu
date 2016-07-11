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
""" 3D display of caribu objects
"""
from matplotlib import pyplot, mpl


try:
    from math import isnan
except ImportError:
    # to be back compatile with python 2.5
    def isnan(num):
        return num != num


import openalea.plantgl.all as pgl
from alinea.caribu.colormap import ColorMap


def _nan_to_zero(values):
    return [0 if isnan(x) else x for x in values]


def plot_color_scale(values, minval=None, maxval=None, label=None):
    """    Produce an plot of a colorscale
    """
    # Make a figure and axes with dimensions as desired.
    fig = pyplot.figure(figsize=(8, 1.5))
    ax1 = fig.add_axes([0.05, 0.4, 0.9, .5])
    if minval is None:
        minval = min(values)
    if maxval is None:
        maxval = max(values)
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=minval, vmax=maxval)
    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                    norm=norm,
                                    orientation='horizontal')
    cb1.set_label(label)
    fig.show()

    return fig


def jet_colors(values, minval=None, maxval=None):
    """return jet colors associated to values after gamme normalisation

    Args:
        values: (list of float) input values
        minval: (float) minimal value at lower bound of color range
        maxval: (float) maximal value at upper bound of color range

    Returns:
        a list of (r, g, b) tuples
    """

    values = _nan_to_zero(values)
    if minval is None:
        minval = min(values)
    if maxval is None:
        maxval = max(values)
    cmap = ColorMap()
    return map(lambda x: cmap(x, minval, maxval, 250., 20.), values)


def generate_scene(triangle_scene, colors=None):
    """ Build a colored PlantGL scene

    Args:
        triangle_scene: (dict of list of list of tuples) a {primitive_id: [triangles, ]} dict,
                each triangle being defined by an ordered triplet of 3-tuple points coordinates.
        colors: (dict of list of tuples) : a {primitive_id: [colors,]} dict
                defining colors of primitives in the scene. A color is a (r, g, b) tuple.

    Returns:
        A plantGL scene of colored shapes
    """
    scene = pgl.Scene()

    if colors is None:
        colors = {k: [(0, 180, 0)] * len(triangle_scene[k]) for k in triangle_scene}
    else:
        if len(triangle_scene) != len(colors):
            raise ValueError('length of triangle_scene and of color should match')

    for k, triangles in triangle_scene.iteritems():
        shape = pgl.TriangleSet([], [])
        shape.colorList = []
        shape.colorPerVertex = False
        shape.id = k
        for i, triangle in enumerate(triangles):
            shape.pointList.append(pgl.Vector3(triangle[0]))
            shape.pointList.append(pgl.Vector3(triangle[1]))
            shape.pointList.append(pgl.Vector3(triangle[2]))
            shape.indexList.append(pgl.Index3(3 * i, 3 * i + 1, 3 * i + 2))
            r, g, b = colors[k][i]
            shape.colorList.append(pgl.Color4(r, g, b, 0))

        scene += shape

    return scene
