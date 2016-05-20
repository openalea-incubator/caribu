"""base Pythonic functions to call caribu shell.
"""

from alinea.caribu.label import Label
from alinea.caribu.caribu_shell import Caribu

green_leaf_PAR = (0.06, 0.07, 0.06, 0.07)
green_stem_PAR = 0.13
soil_reflectance_PAR = 0.2


def pattern_string(pattern_tuple):
    """ format pattern as caribu file string content
    """
    x1, y1, x2, y2 = pattern_tuple
    pattern_tuple = [(min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))]
    pattern = '\n'.join([' '.join(map(str, pattern_tuple[0])),
                         ' '.join(map(str, pattern_tuple[1])), ' '])
    return pattern


def light_string(lights):
    """ format lights as caribu light file string content
    """

    def _as_string(light):
        e, p = light
        return ' '.join(map(str, [e] + list(p))) + '\n'

    if not isinstance(lights, list):
        lights = [lights]
    lines = map(_as_string, lights)

    return ''.join(lines)


def opt_string_and_labels(materials):
    """ format materials as caribu opt file string content and encode label
    """
    opts = {i+1: po for i, po in enumerate(list(set(materials)))}
    n = len(opts)
    opt_string = 'n %s\n' % n
    opt_string += "s d -1\n"
    opts_sorted_keys = sorted(opts.keys())
    for key in opts_sorted_keys:
        po = opts[key]
        if len(po) > 1:
            opt_string += 'e d -1   d %s %s  d %s %s\n' % po
        else:
            opt_string += 'e d %s   d 0.5 0.5  d 0.5 0.5\n' % po

    mapping = {v: k for k, v in opts.iteritems()}

    def _label(material):
        lab = Label()
        lab.plant_id = 1
        lab.optical_id = mapping[material]
        if len(material) > 1:
            lab.leaf_id = 1
        return str(lab)

    labels = [_label(m) for m in materials]

    return opt_string, labels


def triangles_string(triangles, labels):
    """ format triangles and associated labels as caribu canopy string content
    """

    def _can_string(triangle, label):
        s = "p 1 %s 3" % str(label)
        for pt in triangle:
            s += " %.6f %.6f %.6f" % pt
        return s + '\n'

    lines = [_can_string(t, l) for t, l in zip(triangles, labels)]

    return ''.join(lines)


def raycasting(triangles, materials, lights=[(1, (0, 0, -1))], domain=None,
               screen_size=1536):
    """Compute  illumination of triangles using caribu raycasting mode.

    Args:
        triangles: (list of list of tuples) a list of triangles defined
                    by ordered triplets of 3D points coordinates.
        materials: (list of tuple) a list of optical properties of materials
                    of each triangle in a given wavelength.
                    An optical property can be a (reflectance) tuple for opaque materials
                    or  a (reflectance_sup, transmitance_sup, reflectance_inf, transmitance_inf) tuple for translucent materials
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources in a given wavelength
                By default a normalised zenital light is used. Energy is ligth flux passing throuh a unit area horizontal plane.
        domain: (tuple of floats) 2D Coordinates of the domain bounding the scene for its replication.
                 (xmin, ymin, xmax, ymax) scene is not bounded along z axis
                 if None (default), scene is not repeated
        screen_size: (int) buffer size for projection images

    Returns:
        (dict of str:property) properties computed:
          - index(int) : the indices of the input triangles present in outputs ?
          - label(str) : the internal barcode (canlabel) used by caribu (for debuging) 
          - area (float): the indiviual areas of triangles
          - Eabs (float): the surfacic density of energy absorbed by the triangles (absorbed_energy / area) 
          - Ei_inf (float): the surfacic density of energy incoming on the inferior face of the triangle
          - Ei_sup (float): the surfacic density of energy incoming on the superior face of the triangle
    """

    opt_string, labels = opt_string_and_labels(materials)
    can_string = triangles_string(triangles, labels)
    sky_string = light_string(lights)

    if domain is None:
        infinitise = False
        pattern_str = None
    else:
        infinitise = True
        pattern_str = pattern_string(domain)

    caribu = Caribu(canfile=can_string,
                    skyfile=sky_string,
                    optfiles=opt_string,
                    patternfile=pattern_str,
                    direct=True,
                    infinitise=infinitise,
                    projection_image_size=screen_size,
                    debug=True
                    )
    caribu.run()
    out = caribu.nrj

    return out


def radiosity(triangles, materials, lights=(1, (0, 0, -1)), domain=None,
              mixed_radiosity=None,
              screen_size=1536):
    """Compute triangles illumination using radiosity model.

    Args:
        triangles: (list of list of tuples) a list of triangles defined by ordered triplets of 3D points coordinates.
        materials: (list of tuple) a list of optical properties of materials of each triangle in a given wavelength. 
                    An optical property can be a (reflectance) singleton for opaque materials
                    or  a (reflectance_sup, transmitance_sup, reflectance_inf, transmitance_inf) tuple for translucent materials
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources in a given wavelength
                By default a normalised zenital light is used. Energy is ligth flux passing throuh a unit area horizontal plane.
        domain: (tuple of floats) 2D Coordinates of the domain bounding the scene for its replication.
                 (xmin, ymin, xmax, ymax) scene is not bounded along z axis
                 if None (default), scene is not repeated
        mixed_radiosity: (None or tuple) Control of mixed
                         radiosity algorithm.
                         None means do not use mixed radiosity (default)
                         (diameter, nb_layers, height):
                          - diameter: diameter of the spheric neighbourhood of triangles for which pure radiosity is used.
                          - nb_layers: vertical subdivisions of scene used for approximation of far contrbution
                          - height: maximum height of scene layers
        screen_size: (int) buffer size for projection images

    Returns:
        (dict of str:property) properties computed:
          - index(int) : the indices of the input triangles present in outputs ?
          - label(str) : the internal barcode (canlabel) used by caribu (for debuging) 
          - area (float): the indiviual areas of triangles
          - Eabs (float): the surfacic density of energy absorbed by the triangles (absorbed_energy / area) 
          - Ei_inf (float): the surfacic density of energy incoming on the inferior face of the triangle
          - Ei_sup (float): the surfacic density of energy incoming on the superior face of the triangle
    """
    
    opt_string, labels = opt_string_and_labels(materials)
    can_string = triangles_string(triangles, labels)
    sky_string = light_string(lights)

    if domain is None:
        infinitise = False
        pattern_str = None
    else:
        infinitise = True
        pattern_str = pattern_string(domain)
        
    if mixed_radiosity is None:
        diameter = -1
        nb_layers = None
        can_height = None
    else:
        diameter, nb_layers, can_height = mixed_radiosity

    caribu = Caribu(canfile=can_string,
                    skyfile=sky_string,
                    optfiles=opt_string,
                    patternfile=pattern_str,
                    direct=False,
                    infinitise=infinitise,
                    nb_layers=nb_layers,
                    can_height=can_height,
                    sphere_diameter=diameter,
                    projection_image_size=screen_size
                    )
    caribu.run()
    out = caribu.nrj

    return out

