""" Defines messages for deprecated nodes
"""


def GenOutput(etri, eabs):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning('This node is deprecated, use Caribu instead')


def FileCaribuScene(scene, light, pattern, opt):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning('This node is deprecated, use CaribuScene instead')


def ObjCaribuScene(scene, light, pattern, opt, waveLength):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning('This node is deprecated, use CaribuScene instead')


def getEi(cs):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning(
        'This node is deprecated, use getIncidentEnergy instead')

def MCSail(sail_scene, sleep):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning(
        'This node is deprecated, mcsail/sailscene wrapper code has been droped from package in july 2016')

def S2v(caribuscene, nlayers, zlayer, sleep):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning(
        'This node is deprecated, s2v wrapper code has been droped in july 2016')

def Canestra(caribuscene, sailfluxes, direct, s_sphere, keepFF):
    """ This is a deprecated node, not functional anymore"""
    raise DeprecationWarning(
        'This node is deprecated, canestra wrapper code has been droped in july 2016')