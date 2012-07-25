"""Functional Interfaces to CaribuScene class methods
Theses interfaces are mainly tageted for building visualea nodes
They generally have an additional copyscene argument, that pass caribuscene by copy instead of by reference

"""
from copy import copy
#alternative a local importt de caribuscene ne serait il pas de faire import * ici , par hasard??
from CaribuScene import CaribuScene, CaribuSceneError

class CaribuSceneDeprecatedError(CaribuSceneError): pass

#caribuscene instance used to access doc strings of class methods
cdoc = CaribuScene()

def newCaribuScene(scene,light,pattern,opt):
    cs = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    mapid = dict(zip(cs.scene_labels,cs.scene_ids))
    return cs, mapid
docadd = '\n\nreturn a caribuscene object and a map of primitiveid-> caribu internal ids\n'
newCaribuScene.__doc__ = ''.join([cdoc.__init__.__doc__,docadd])

   
def addShapes(caribuscene,shapes,tesselator, canlabels, copyscene):    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
        
    mid=cs.add_Shapes(shapes,tesselator,canlabels)
    
    return cs,mid 
addShapes.__doc__ = cdoc.add_Shapes.__doc__
    
    
def addSoil(caribuscene, zsoil, copyscene):
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    
    mid = cs.addSoil(zsoil)
    
    return cs,mid
addSoil.__doc__ = cdoc.addSoil.__doc__
 
 
def WriteCan(caribuscene, filename):    
    caribuscene.writeCan(filename)
    return filename
WriteCan.__doc__ = cdoc.writeCan.__doc__
    
    
def output_by_id(caribuscene,mapid,aggregate):
    return caribuscene.output_by_id(mapid,aggregate)
output_by_id.__doc__ = cdoc.output_by_id.__doc__


def runCaribu(caribuscene, direct, scatterOpt, copyscene):
    """functional interface to Caribu    
    """
    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
     
    nz,dz,ds = scatterOpt['Nz'], scatterOpt['Zmax'], scatterOpt['SphereDiameter']
    cs.runCaribu(direct,nz,dz,ds)
    
    return cs,cs.output



def getIncidentEnergy(caribuscene):
        """ Compute Qi, Qem, Einc on the scene given current light sources.

        Qi is the incident light flux received on an horizontal surface (per scene unit area)
        Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
        Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set

        """    
        return caribuscene.getIncidentEnergy()

# future deprecated nodes

def newFileCaribuScene(scene,light,pattern,opt):
    """ Warning !!! This node is deprecated and will be removed in future versions, use CaribuScene instead."""
    print('Warning !!! FileCaribuScene is deprecated and will be removed in future versions, use CaribuScene instead')
    cs,mapid=newCaribuScene(scene,light,pattern,opt)
    return cs,mapid
    
#deprecated nodes (used to inform user of alternatives)

def GenOutput(etri,eabs):
    """ This is a deprecated node, not functional anymore"""
    raise CaribuSceneDeprecatedError('This node is deprecated, use vcaribu/caribu interfaces to Canestra')