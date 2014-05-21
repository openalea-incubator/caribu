from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.label import simple_canlabel
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

def diffuse_source(directions = 1):
    energie, emission, direction, elevation, azimuth = turtle.turtle(sectors=str(directions), energy=1) 
    return zip(energie,direction)
    
    
def caribu_lighted_scene(scene, directions = 1, domain = None, minval=None, maxval=None):
    """ generate a per-triangle colored lighted scene  (like ViewMapOnCan)
    """
    # This import makes matplotlib with TkAgg frontend crash for some mysterious reason : don't import it on top
    from openalea.color.colormap import ColorMap
    energie, emission, direction, elevation, azimuth = turtle.turtle(sectors=str(directions), energy=1) 
    sources = zip(energie,direction)
    
    c_scene = CaribuScene(pattern = domain)
    idmap = c_scene.add_Shapes(scene)    
    c_scene.addSources(sources)
    ifty = False
    if domain is not None:
        ifty = True
        
    output = c_scene.runCaribu(infinity=ifty)
    eabs = output['Eabsm2']
    if minval is None:
        minval = min(eabs)
    if maxval is None:
        maxval = max(eabs)
    cmap = ColorMap()
    colors = map(lambda x: cmap(x,minval,maxval,250., 20.),eabs)
    return c_scene.generate_scene(colors)


def run_caribu(sources, scene, opticals = 'stem', optical_properties=None, output_by_triangle = False, domain = None, zsoil=None):
    """ 
    Calls Caribu for differents energy sources

    :Parameters:
    ------------
    - `sources` (int)
    - `scene` : any scene format accepted by CaribuScene. This will be cast to a list of plantGL shapes
    - opticals : a list of optical property labels ('leaf', 'soil', 'stem', 'ear' or 'awn') for all shapes in scene. If a shorter opticale list is provided, it will be recycled to match eength of shape list
    - `optical_properties`: a filename (*.opt), a string (opt file format) or a dict. 
      If optical_properties is a dict, its structure is: {species: (r_opaque, r_translucent_sup, t_translucent_sup, r_translucent_inf, t_translucent_inf)}
      species is: 's' for soil, 'e1' for species 1, 'e2' for species 2, and so on. If species == 's' (i.e. soil), then just r_opaque is required.   
    - `output_by_triangle` (bool) 
        Default 'False'. Return is done by id of geometry. If 'True', return is done by triangle. 

    :Returns:
    ---------
    - 'out_moy' (dict)
        A dict of intercepted variable (energy) per id
    - 'out_tri' (dict) only if output_by_triangle = True, return a tuple (out_moy, out_tri)
        A dict of intercepted variable (energy) per triangle
    """
    c_scene = CaribuScene(pattern = domain, opt=optical_properties)
        
    if not isinstance(opticals, list):
        opticals = [opticals]
    if len(opticals) < len(scene):
        opticals = opticals * (len(scene) / len(opticals)) + [opticals[i] for i in range(len(scene) % len(opticals))]
    
    labels = [simple_canlabel(opt) for opt in opticals]
    idmap = c_scene.add_Shapes(scene, canlabels=labels)    
    c_scene.addSources(sources)
    
    ifty = False
    if domain is not None:
        ifty = True
        if zsoil is not None:
            idmap_soil = c_scene.addSoil(zsoil=zsoil)
            idmap.update(idmap_soil)
        
    output = c_scene.runCaribu(infinity=ifty)
    
    if output_by_triangle:
        out = c_scene.output_by_id(output, idmap, aggregate = False)
    else:
        out = c_scene.output_by_id(output, idmap)
    return out

# add two entry po and sources po 
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

def caribu_light_star(g, light_sectors='16', output_by_triangle = False, domain = None, convUnit = 0.01, trigger = 1):
    geom = g.property('geometry')
    light_star, light_exposed_area = caribu_star(geom, directions = light_sectors, output_by_triangle=output_by_triangle, convUnit=convUnit, domain = domain)
    if not 'light_exposed_area' in g.properties():
        g.add_property('light_exposed_area')
    if not 'light_star' in g.properties():
        g.add_property('light_star')
    g.property('light_exposed_area').update(light_exposed_area)
    g.property('light_star').update(light_star)
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


    