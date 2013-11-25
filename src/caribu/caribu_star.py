from openalea.plantgl import all as pgl
from alinea.caribu.CaribuScene import CaribuScene
import alinea.caribu.sky_tools.turtle as turtle
from math import radians, degrees, sin , cos



def vecteur_direction(elevation,azimuth):
    theta = radians(90 - elevation)
    phi = radians(azimuth)
    return sin(theta) * cos(phi),sin(theta) * sin(phi),  -cos(theta)


def emission_inv(elevation, energy):
    """ return energy of emmision for a source of a given direction and of a given energy received on a horizontal surface """
    theta = radians(90 - elevation)
    received_energy = energy * abs(cos(theta))
    return received_energy


def geom2shape(vid, mesh):
    """ Create a shape """
    shape = pgl.Shape(mesh)
    shape.id = vid
    return shape


def run_caribu(sources, scene_geometry, output_by_triangle = False, domain = None):
    """ 
    Calls Caribu for differents energy sources

    :Parameters:
    ------------
    - `sources` (int)
    - `scene_geometry`
    - `output_by_triangle` (bool) 
        Default 'False'. Return is done by id of geometry. If 'True', return is done by triangle. 

    :Returns:
    ---------
    - 'out_moy' (dict)
        A dict of intercepted variable (energy) per id
    - 'out_tri' (dict) only if output_by_triangle = True, return a tuple (out_moy, out_tri)
        A dict of intercepted variable (energy) per triangle
    """
    c_scene = CaribuScene(pattern = domain)
    shapes=[geom2shape(k,v) for k,v in scene_geometry.iteritems()]
    idmap = c_scene.add_Shapes(shapes)    
    c_scene.addSources(sources)
    ifty = False
    if domain is not None:
        ifty = True
    output = c_scene.runCaribu(infinity=ifty)
    
    if output_by_triangle:
        out = c_scene.output_by_id(output, idmap, aggregate = False)
    else:
        out = c_scene.output_by_id(output, idmap)
    return out


def caribu_star(scene_geometry, directions = 1, output_by_triangle = False, domain = None, convUnit = 0.01):
    """ 
    Compute exposition ('surface_viewed-to_area ratio and exposed surface(m2)') of scene elements from a given number of direction

    :Parameters:
    ------------
    - `sectors` (int) : number of directions (1, 16 or 46)
    - `scene_geometry`
    - 'output_by_triangle' (bool)
        Default 'False'. Choose if return dict(id:exosition) or dict(id:[expositions_of_triangles])
    - 'convUnit' (float)
        Default '0.01'. Conversion factor to get meter from scene length unit.

    :Returns:
    ---------
    - a dict id:star (ratio viewed area / area) and id:exposed_surface (m2)
    """
    energie, emission, direction, elevation, azimuth = turtle.turtle(sectors=str(directions), energy=1) 
    sources = zip(energie,direction)
    out = run_caribu(sources, scene_geometry, output_by_triangle=output_by_triangle, domain = domain)
    star = out['Ei']
    areas = out['Area']
    if output_by_triangle:
        exposed_area = {vid: [star[vid][i] * areas[vid][i] * convUnit**2 for i in range(len(areas[vid]))] for vid in areas}
    else:
        exposed_area = {vid: star[vid] * areas[vid] * convUnit**2 for vid in areas}
    return star, exposed_area

def caribu_rain_star(g, output_by_triangle = False, domain = None, convUnit = 0.01, dt = 1):
    geom = g.property('geometry')
    rain_star, rain_exposed_area = caribu_star(geom, directions = 1, output_by_triangle=output_by_triangle, convUnit=convUnit, domain = domain)
    if not 'rain_exposed_area' in g.properties():
        g.add_property('rain_exposed_area')
    if not 'rain_star' in g.properties():
        g.add_property('rain_star')
    g.property('rain_exposed_area').update(rain_exposed_area)
    g.property('rain_star').update(rain_star)
    return g

    
def rain_and_light_star(g, light_sectors='16', output_by_triangle = False, domain = None, convUnit = 0.01, trigger = 1):
    geom = g.property('geometry')
    rain_star, rain_exposed_area = caribu_star(geom, directions = 1, output_by_triangle=output_by_triangle, convUnit=convUnit, domain = domain)
    if light_sectors == '1':
        light_star, light_exposed_area = rain_star, rain_exposed_area
    else:
        light_star, light_exposed_area = caribu_star(geom, directions = light_sectors, output_by_triangle=output_by_triangle, convUnit=convUnit, domain = domain)
    if not 'rain_exposed_area' in g.properties():
        g.add_property('rain_exposed_area')
    if not 'rain_star' in g.properties():
        g.add_property('rain_star')
    if not 'light_exposed_area' in g.properties():
        g.add_property('light_exposed_area')
    if not 'light_star' in g.properties():
        g.add_property('light_star')
    g.property('rain_exposed_area').update(rain_exposed_area)
    g.property('light_exposed_area').update(light_exposed_area)
    g.property('rain_star').update(rain_star)
    g.property('light_star').update(light_star)
    return g

    
    