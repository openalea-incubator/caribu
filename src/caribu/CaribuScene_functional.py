"""Functional Interfaces to CaribuScene class methods
Theses interfaces are mainly tageted for building visualea nodes
They generally have an additional copyscene argument, that pass caribuscene by copy instead of by reference

"""
from copy import copy
from CaribuScene import CaribuScene


def newCaribuScene(scene,light,pattern,opt):
    """ Creates and Initialise a Caribu Scene object.
        scene is a filename (*.can), a string (can file format) or a PlantGl scene/shape
        ligth is a filename (*.light), a string (light file format) or a (list of) tuple (Energy, (vx, vy, vz))
        pattern is a filename (*.8), a string (8 file format) or a tuple ((xmin,ymin), (xmax,ymax))
        opt is a filename (*.opt) or a string (opt file format)
        
        File format specifications are in data/CanestraDoc.pdf
    
    """
    cs = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    return cs
   

def newFileCaribuScene(scene,light,pattern,opt):
    """ Warning !!! This node is deprecated and will be removed in future versions, use CaribuScene instead."""
    cs=CaribuScene(scene=scene,light=light,pattern=pattern,opt=opt)
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
    return caribuscene



def getIncidentEnergy(caribuscene):
        """ Compute Qi, Qem, Einc on the scene given current light sources.

        Qi is the incident light flux received on an horizontal surface (per scene unit area)
        Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
        Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set

        """    
        return caribuscene.getIncidentEnergy()

