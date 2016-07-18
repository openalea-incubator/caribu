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
