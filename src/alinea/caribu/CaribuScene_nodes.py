"""Functional Interfaces to CaribuScene class methods
Theses interfaces are mainly tageted for building visualea nodes
They generally have an additional copyscene argument, that pass caribuscene by copy instead of by reference

"""
from copy import copy
from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.display import generate_scene


#caribuscene instance used to access doc strings of class methods
cdoc = CaribuScene()


def newCaribuScene(scene=None, light=[(1, (0, 0, -1))], pattern=None,
                   opt={'band1': (0.06, 0.07)},
                   soil_reflectance={'band1': 0.15},
                   soil_mesh=-1, z_soil=0., scene_unit='cm'):
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
    d_sphere, layers, height = scatterOpt['d_sphere'], scatterOpt['height'], \
                               scatterOpt['d_sphere']
    raw, aggregated = caribuscene.run(direct=direct, infinite=infinite,
                                        d_sphere=d_sphere, layers=layers,
                                        height=height, screen_size=screen_size,
                                        split_face=split_face,
                                        simplify=simplify)
    return caribuscene, aggregated, raw
runCaribu.__doc__ = cdoc.run.__doc__


def resetScene(caribuscene, copyscene):
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    cs.resetScene()
    return cs
# resetScene.__doc__ = ''.join([cdoc.resetScene.__doc__, copyscenedoc])
   
def addShapes(caribuscene,shapes,tesselator, canlabels, autocan, copyscene):    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene

    if autocan:
        canlabels = None
     
    mid=cs.add_Shapes(shapes,tesselator,canlabels)
    
    return cs,mid 
# addShapes.__doc__ = ''.join([cdoc.add_Shapes.__doc__, copyscenedoc])
    
    
def addSoil(caribuscene, zsoil, copyscene):
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    
    mid = cs.addSoil(zsoil)
    
    return cs,mid
# addSoil.__doc__ = ''.join([cdoc.addSoil.__doc__, copyscenedoc])
 
 
def WriteCan(caribuscene, filename):    
    caribuscene.writeCan(filename)
    return filename
# WriteCan.__doc__ = cdoc.writeCan.__doc__
    
    
def output_by_id(caribuscene,output,mapid,groups,aggregate):
    return caribuscene.output_by_id(output,mapid,groups,aggregate)
# output_by_id.__doc__ = cdoc.output_by_id.__doc__




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

   
def getIncidentEnergy(caribuscene):
        return caribuscene.getIncidentEnergy()
# getIncidentEnergy.__doc__ = cdoc.getIncidentEnergy.__doc__




