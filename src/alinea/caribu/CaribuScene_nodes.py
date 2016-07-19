"""Functional Interfaces to CaribuScene class methods
Theses interfaces are mainly tageted for building visualea nodes
They generally have an additional copyscene argument, that pass caribuscene by copy instead of by reference

"""
from copy import copy
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.display import generate_scene
from alinea.caribu.caribu import opt_string_and_labels, triangles_string


#caribuscene instance used to access doc strings of class methods
cdoc = CaribuScene()


def newCaribuScene(scene=None, light=[(1, (0, 0, -1))], pattern=None,
                   opt={'band1': (0.06, 0.07)},
                   soil_reflectance={'band1': 0.15},
                   soil_mesh=-1, z_soil=0., scene_unit='cm'):
    # backward compatibility for opt file
    if isinstance(opt, str):
        opt = [opt]
    return CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt,
                     soil_reflectance=soil_reflectance, soil_mesh=soil_mesh,
                     z_soil=z_soil, scene_unit=scene_unit)
newCaribuScene.__doc__ = cdoc.__init__.__doc__


def runCaribu(caribuscene, direct=True,
              scatterOpt={'d_sphere': 0.5, 'layers': 5, 'height': None},
              infinite=False, screen_size=1536, split_face=False,
              simplify=True):
    if caribuscene is None:
        return None, {}, {}
    d_sphere, layers, height = None, None, None
    if not direct:
        try:
            d_sphere, layers, height = scatterOpt['d_sphere'], scatterOpt['layers'], \
                                   scatterOpt['height']
        except KeyError:
            raise KeyError("""keys of scatterOptions have changed,
            please rename input dict keys as follow:
            - SphereDiameter -> d_sphere
            - Nz -> layers
            - Zmax -> height""")

    raw, aggregated = caribuscene.run(direct=direct, infinite=infinite,
                                        d_sphere=d_sphere, layers=layers,
                                        height=height, screen_size=screen_size,
                                        split_face=split_face,
                                        simplify=simplify)
    return caribuscene, aggregated, raw
runCaribu.__doc__ = cdoc.run.__doc__


def getIncidentEnergy(caribuscene):
        return caribuscene.getIncidentEnergy()
getIncidentEnergy.__doc__ = cdoc.getIncidentEnergy.__doc__


def getSoilEnergy(caribuscene):
        return caribuscene.getSoilEnergy()
getIncidentEnergy.__doc__ = cdoc.getSoilEnergy.__doc__


def selectOutput(output, variable='Ei', band=None):
    """ select an output of Caribu

    Args:
        output: a caribu output (raw or aggregated)
        variable(str): the name of the output varaible (see details)
        band (str): None (default) if the result is a simplified one, or the name
         of the band

    Returns:
        A property dict of the output
        the name of the output variable

    Details:
    output variables are:
        - area (float): the individual areas (m2)
        - Eabs (float): the surfacic density of energy absorbed (m-2)
        - Ei (float): the surfacic density of energy incoming (m-2)
    additionally, if split_face was set to True:
        - Ei_inf (float): the surfacic density of energy incoming
          on the inferior face (m-2)
        - Ei_sup (float): the surfacic density of energy incoming
           on the superior face (m-2)
    """
    if band is not None:
        try:
            output = output[band]
        except KeyError:
            pass
    return output[variable], variable

def ViewMapOnCan(caribuscene, property, gamma=None, minval=None, maxval=None):
    """

    Args:
        caribuscene: a CaribuScene instance
        property: a dict of values,
                each key being a scene primitive index.
        gamma: exponent of the normalised values
                    if None (default), na gamma transform is applied
        minval: (float) minimal value at lower bound of color range
                    if None (default), minimal value of property is used
        maxval: float) maximal value at upper bound of color range
                    if None (default), maximal value of property is used

    Returns:
        caribu_scene object
        plantGL scene
    """
    scene, values = caribuscene.plot(property, minval, maxval, gamma, display=True)
    return caribuscene, scene, values

 
 
def WriteCan(caribuscene, filename):
    o_string, labels = opt_string_and_labels(caribuscene.material)
    can_string = triangles_string(caribuscene.scene, labels)
    with open(filename, 'w') as output:
        output.write(can_string)
    return filename




def periodise(caribuscene, copyscene):
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    
    cs.runPeriodise()
    return cs
# periodise.__doc__ =''.join([cdoc.runPeriodise.__doc__,copyscenedoc])

   
def generate_scene_node(caribuscene, colors):
    return generate_scene(caribuscene.scene, colors)

   





