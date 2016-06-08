""" 3D display of caribu objects
"""
from matplotlib import pyplot, mpl

import openalea.plantgl.all as pgl
from alinea.caribu.colormap import ColorMap


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

    if minval is None:
        minval = min(values)
    if maxval is None:
        maxval = max(values)
    cmap = ColorMap()
    return map(lambda x: cmap(x, minval, maxval, 250., 20.), values)


def generate_scene(triangles, groups=None, colors=None):
    """ Build a PlantGL scene object structured by groups with colors

    Args:
        triangles: (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
        groups: (list of int) a list indicating the group the triangles belongs to.
                if None (default) one shape  per triangle is created, otherwise one shape per group.
        colors: (list of list of tuples) : a list of (r, g, b) color tuples.
                if groups is None (default), each tuple indicate the color a triangle
                If groups is not None, each tuple indicates  the color of a group

    Returns:
        A plantGL scene of colored shapes
    """
    scene = pgl.Scene()

    if groups is None:
        if colors is None:
            colors = [(0, 180, 0)] * len(triangles)
        else:
            if len(triangles) != len(colors):
                raise ValueError('length of triangle list and of color list should match when groups is None')

        for i, triangle in enumerate(triangles):
            points = [pgl.Vector3(triangle[i]) for i in range(2)]
            indices = [pgl.Index3(0, 1, 2)]
            geometry = pgl.TriangleSet(points, indices)
            material = pgl.Material(pgl.Color3(*colors[i]))
            shape = pgl.Shape(geometry, material)
            shape.id = i
            scene += shape
    else:
        if colors is None:
            colors = [(0, 180, 0)] * len(set(groups))
        else:
            if len(set(groups)) != len(colors):
                raise ValueError('length of color list and the number of dictinct groups should match')

        geometries = {}
        for i, triangle in enumerate(triangles):
            group = groups[i]
            if group not in geometries:
                geometries[group] = pgl.TriangleSet([], [])
            geometry = geometries[group]
            count = len(geometry.pointList)
            geometry.pointList.append(pgl.Vector3(triangle[0]))
            geometry.pointList.append(pgl.Vector3(triangle[1]))
            geometry.pointList.append(pgl.Vector3(triangle[2]))
            geometry.indexList.append(pgl.Index3(count, count + 1, count + 2))
        for group, geometry in geometries.iteritems():
            material = pgl.Material(pgl.Color3(*colors[group]))
            shape = pgl.Shape(geometry, material)
            shape.id = group
            scene += shape

    return scene
