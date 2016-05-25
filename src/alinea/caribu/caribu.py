"""base Pythonic functions to call caribu shell.
"""

from alinea.caribu.label import Label
from alinea.caribu.caribu_shell import Caribu

green_leaf_PAR = (0.06, 0.07)
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

    
def opt_string(species):
    """ format species as caribu opt file string content
    """
   
    n = len(species)
    o_string = 'n %s\n' % n
    o_string += "s d -1\n"
    species_sorted_keys = sorted(species.keys())
    for key in species_sorted_keys:
        po = species[key]
        if hasattr(po,'__iter__'):
            if len(po) == 2:
                o_string += 'e d -1   d %s %s' % po + ' d %s %s\n' % po
            else:
                o_string += 'e d -1   d %s %s  d %s %s\n' % po
        else:
            o_string += 'e d %s   d -1 -1  d -1 -1\n' % po
    
    return o_string

    
def encode_labels(materials, species):
    def _label(material):
        lab = Label()
        lab.plant_id = 1
        lab.optical_id = mapping[material]
        if hasattr(material,'__iter__'):
            lab.leaf_id = 1
        return str(lab)
    mapping = {v: k for k, v in species.iteritems()} 
    return [_label(m) for m in materials]    

    
def opt_string_and_labels(materials):
    """ format materials as caribu opt file string content and encde label
    """  

    species = {i+1: po for i, po in enumerate(list(set(materials)))}    
    o_string = opt_string(species)
    labels = encode_labels(materials, species)
    
    return o_string, labels
    
def x_opt_strings_and_labels(x_materials):
    """ format multispectral materials as caribu opt file strings content
    """
     
    x_opts = zip(*x_materials.values())
    x_species = {i+1: po for i, po in enumerate(list(set(x_opts)))}

    labels = encode_labels(x_opts, x_species)
    
    opt_strings = {}
    for i, k in enumerate(x_materials.keys()):      
        species = {k:v[i] for k,v in x_species.iteritems()}
        opt_strings[k] = opt_string(species)
    
    return opt_strings, labels    

    
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
    """Compute monochrome illumination of triangles using caribu raycasting mode.

    Args:
        triangles: (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
        materials: (list of tuple) a list of materials defining optical properties of triangles
                    A material is a 1-, 2- or 4-tuple depending on its optical behavior.
                    A 1-tuple encode the reflectance of an opaque material
                    A 2-tuple encode the reflectance and transmittance of a symetric translucent material
                    A 4-tuple encode the reflectance and transmittance                     
                    of the upper and lower side of an asymetric translucent material
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources
                By default a normalised zenital light is used. 
                Energy is ligth flux passing throuh a unit area horizontal plane.
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

    if len(triangles) != len(materials):
        raise ValueError('The number of triangles and materials should match')
    
    o_string, labels = opt_string_and_labels(materials)
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
                    optfiles=o_string,
                    patternfile=pattern_str,
                    direct=True,
                    infinitise=infinitise,
                    projection_image_size=screen_size,
                    )
    caribu.run()
    out = caribu.nrj['band0']['data']

    return out


def radiosity(triangles, materials, lights=(1, (0, 0, -1)), screen_size=1536):
    """Compute monochromatic illumination of triangles using radiosity method.

    Args:
        triangles: (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
        materials: (list of tuple) a list of materials defining optical properties of triangles
                    A material is a 1-, 2- or 4-tuple depending on its optical behavior.
                    A 1-tuple encode an opaque material characterised by its reflectance
                    A 2-tuple encode a symetric translucent material defined by a reflectance and a transmittance 
                    A 4-tuple encode an asymetric translucent material defined the reflectance and transmittance                     
                    of the upper and lower side respectively
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources
                By default a normalised zenital light is used. 
                Energy is ligth flux passing throuh a unit area horizontal plane.
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
    
    if len(triangles) <= 1:
        raise ValueError('Radiosity method needs at least two primitives')
    
    if len(triangles) != len(materials):
        raise ValueError('The number of triangles and materials should match')
    
    o_string, labels = opt_string_and_labels(materials)
    can_string = triangles_string(triangles, labels)
    sky_string = light_string(lights)

    caribu = Caribu(canfile=can_string,
                    skyfile=sky_string,
                    optfiles=o_string,
                    patternfile=None,
                    direct=False,
                    infinitise=False,
                    sphere_diameter=-1,
                    projection_image_size=screen_size
                    )
    caribu.run()
    out = caribu.nrj['band0']['data']

    return out

    
def x_radiosity(triangles, x_materials, lights=(1, (0, 0, -1)), screen_size=1536):
    """Compute multi-chromatic illumination of triangles using radiosity method.

    Args:
        triangles: (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
        x_materials: (dict of list of tuple) a {band_name: [materials]} dict defining optical properties of triangles 
                    for different band/wavelength
                    A material is a 1-, 2- or 4-tuple depending on its optical behavior.
                    A 1-tuple encode an opaque material characterised by its reflectance
                    A 2-tuple encode a symetric translucent material defined by a reflectance and a transmittance 
                    A 4-tuple encode an asymetric translucent material defined the reflectance and transmittance                     
                    of the upper and lower side respectively
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources
                By default a normalised zenital light is used. 
                Energy is ligth flux passing throuh a unit area horizontal plane.
        screen_size: (int) buffer size for projection images

    Returns:
        (a {band_name: {property_name:property_values}} dict of dict) with  properties:
          - index(int) : the indices of the input triangles present in outputs ?
          - label(str) : the internal barcode (canlabel) used by caribu (for debuging) 
          - area (float): the indiviual areas of triangles
          - Eabs (float): the surfacic density of energy absorbed by the triangles (absorbed_energy / area) 
          - Ei_inf (float): the surfacic density of energy incoming on the inferior face of the triangle
          - Ei_sup (float): the surfacic density of energy incoming on the superior face of the triangle
    """
    
    if len(triangles) <= 1:
        raise ValueError('Radiosity method needs at least two primitives')
    
    if len(triangles) != len(materials):
        raise ValueError('The number of triangles and materials should match')
    
    
    opt_strings, labels = x_opt_strings_and_labels(x_materials)
    can_string = triangles_string(triangles, labels)
    sky_string = light_string(lights)

    caribu = Caribu(canfile=can_string,
                    skyfile=sky_string,
                    optfiles=opt_strings.values(),
                    optnames=opt_strings.keys(),
                    patternfile=None,
                    direct=False,
                    infinitise=False,
                    sphere_diameter=-1,
                    projection_image_size=screen_size
                    )
    caribu.run()
    out = {k:v['data'] for k,v in caribu.nrj.iteritems()}

    return out

    
def mixed_radiosity(triangles, materials, lights, domain,
              diameter, layers, height, screen_size=1536):
    """Compute monochrome illumination of triangles using radiosity model.

    Args:
        triangles: (list of list of tuples) a list of triangles, each being defined
                    by an ordered triplet of 3-tuple points coordinates.
        materials: (list of tuple) a list of materials defining optical properties of triangles
                    A material is a 1-, 2- or 4-tuple depending on its optical behavior.
                    A 1-tuple encode an opaque material characterised by its reflectance
                    A 2-tuple encode a symetric translucent material defined by a reflectance and a transmittance 
                    A 4-tuple encode an asymetric translucent material defined the reflectance and transmittance                     
                    of the upper and lower side respectively
        lights: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining ligh sources
                Energy is ligth flux passing throuh a unit area horizontal plane.
        domain: (tuple of floats) 2D Coordinates of the domain bounding the scene for its replication.
                 (xmin, ymin, xmax, ymax) scene is not bounded along z axis
        diameter: diameter of the sphere defining the close neighbourhood for local radiosity.
        nb_layers: vertical subdivisions of scene used for approximation of far contrbution
        height: upper limit of canopy layers
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
    
    if len(triangles) <= 1:
        raise ValueError('Radiosity method needs at least two primitives')
    
    if len(triangles) != len(materials):
        raise ValueError('The number of triangles and materials should match')
    
    o_string, labels = opt_string_and_labels(materials)
    can_string = triangles_string(triangles, labels)
    sky_string = light_string(lights)
    pattern_str = pattern_string(domain)

    caribu = Caribu(canfile=can_string,
                    skyfile=sky_string,
                    optfiles=o_string,
                    patternfile=pattern_str,
                    direct=False,
                    infinitise=True,
                    nb_layers=layers,
                    can_height=height,
                    sphere_diameter=diameter,
                    projection_image_size=screen_size
                    )
    caribu.run()
    out = caribu.nrj['band0']['data']

    return out