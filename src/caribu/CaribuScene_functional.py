"""Functional Interfaces to CaribuScene class methods
Theses interfaces are mainly tageted for building visualea nodes
They generally have an additional copyscene argument, that pass caribuscene by copy instead of by reference

"""
from copy import copy
from CaribuScene import CaribuScene, CaribuSceneError

class CaribuSceneDeprecatedError(CaribuSceneError): pass

def newCaribuScene(scene,light,pattern,opt):
    """ Creates and Initialise a Caribu Scene object.
        scene is a filename (*.can), a string (can file format) or a PlantGl scene/shape
        ligth is a filename (*.light), a string (light file format) or a (list of) tuple (Energy, (direction_x, direction_y, direction_z))
        pattern is a filename (*.8), a string (8 file format) or a tuple ((xmin,ymin), (xmax,ymax))
        opt is a filename (*.opt) or a string (opt file format)
        
        File format specifications are in data/CanestraDoc.pdf
    
    """
    cs = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    return cs
   
    
def addShapes(caribuscene,shapes,tesselator, canlabels, copyscene):
    """Add shapes to scene and return a map of shapes id to carbu internal ids.
   
    """
    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
        
    mid=cs.add_Shapes(shapes,tesselator,canlabels)
    
    return cs,mid 

def addSoil(caribuscene, zsoil, copyscene):
    """ Add Soil to Caribu scene. Soil dimension is taken from pattern """
    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    
    mid = cs.addSoil(zsoil)
    
    return cs,mid
    
def WriteCan(caribuscene, filename):
    """  write the scene in a file (can format).""" 
    caribuscene.writeCan(filename)
    return filename,
    
def getOutput(caribuscene,var,aggregate):
    return caribuscene.getOutput(var,aggregate)


def runCaribu(caribuscene, direct, nz, dz, ds, copyscene):
    """functional interface to Caribu    
    """
    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
     
    caribuscene.run(direct,nz,dz,ds)
    return cs



def getIncidentEnergy(caribuscene):
        """ Compute Qi, Qem, Einc on the scene given current light sources.

        Qi is the incident light flux received on an horizontal surface (per scene unit area)
        Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
        Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set

        """    
        return caribuscene.getIncidentEnergy()

# Deprecated / future deprecated nodes

def newFileCaribuScene(scene,light,pattern,opt):
    """ Warning !!! This node is deprecated and will be removed in future versions, use CaribuScene instead."""
    print('Warning !!! FileCaribuScene is deprecated and will be removed in future versions, use CaribuScene instead')
    cs=CaribuScene(scene=scene,light=light,pattern=pattern,opt=opt)
    return cs
    
def GenOutput(etri,eabs):
    """ This is a deprecated node, not functional anymore"""
    raise CaribuSceneDeprecatedError('This node is deprecated, use vcaribu/caribu interfaces to Canestra/McSail')