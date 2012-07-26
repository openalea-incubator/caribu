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


def runCaribu(caribuscene, direct, scatterOpt, infinity, copyscene):
    """High level interface to Caribu script
        Caribu implements the nested radiosity model
        returns updated caribuscene and the results for the first wavelength computed
    """
    
    if copyscene:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
     
    nz,dz,ds = scatterOpt['Nz'], scatterOpt['Zmax'], scatterOpt['SphereDiameter']
    cs.runCaribu(direct,nz,dz,ds,infinity)
    
    return cs,cs.output


def getIncidentEnergy(caribuscene):
        return caribuscene.getIncidentEnergy()
getIncidentEnergy.__doc__ = cdoc.getIncidentEnergy.__doc__

# future deprecated nodes

def newFileCaribuScene(scene,light,pattern,opt):
    """ This node is deprecated and will be removed in future versions, use CaribuScene instead."""
    print('Warning !!! FileCaribuScene is deprecated and will be removed in future versions, use CaribuScene instead')
    cs,mapid=newCaribuScene(scene,light,pattern,opt)
    return cs,mapid

def newObjCaribuScene(scene,ligth,pattern,opt,waveLength):
    """ This node is deprecated and will be removed in future versions, use CaribuScene instead."""
    print('Warning !!! ObjCaribuScene is deprecated and will be removed in future versions, use CaribuScene instead')
    cs,mapid=newCaribuScene(scene,light,pattern,opt)
    cs.wavelength = waveLength
    return cs,mapid

def getEi(cs):
    """ This node is deprecated and will be removed in future versions, use getIncidentEnergy instead."""
    print('Warning !!! getEi is deprecated and will be removed in future versions, use getIncidentEnergy instead')
    qi,qe,ei = cs.getIncidentEnergy()
    return qi
    
#deprecated nodes (used to inform user of alternatives)

def GenOutput(etri,eabs):
    """ This is a deprecated node, not functional anymore"""
    raise CaribuSceneDeprecatedError('This node is deprecated, use vcaribu/caribu interfaces to Canestra')