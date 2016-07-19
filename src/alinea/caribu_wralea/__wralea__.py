
# This file has been generated at Sat Aug 04 18:13:50 2012

from openalea.core import *


__name__ = 'alinea.caribu'

__editable__ = True
__description__ = ' Caribu package '
__license__ = ''
__url__ = ''
__alias__ = ['Caribu']
__version__ = '0.0.4'
__authors__ = 'M. Chelle,C. Fournier'
__institutes__ = 'INRA'
__icon__ = 'Caribou.png'


__all__ = []

CaribuScene_nodes_CaribuScene = Factory(name='CaribuScene',
                authors='C. Fournier',
                description='instantiate a CaribuScene object',
                category='scene.light',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='newCaribuScene'
               )
__all__.append('CaribuScene_nodes_CaribuScene')


CaribuScene_nodes_runCaribu = Factory(name='Caribu',
                authors='C. Fournier',
                description='',
                category='scene.light',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='runCaribu',
                outputs=[{'name':'CaribuScene'},
                         {'name':'aggregated output'},
                         {'name': 'raw (per triangle) output'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('CaribuScene_nodes_runCaribu')



caribu_vcaribu = Factory(name='vcaribu',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Visualea interface to Caribu class',
                category='scene.light',
                nodemodule='alinea.caribu.caribu_shell',
                nodeclass='vcaribu',
                inputs=[{'interface': IFileStr, 'name': 'canopy', 'value': None, 'desc': "file '.can' or file content representing the 3d scene"},
                        {'interface': IFileStr, 'name': 'lightsource', 'value': None, 'desc': 'file or file content describing light sources (direction, irradiance)'},
                        {'interface': None, 'name': 'optics', 'value': None, 'desc': 'list of files/files contents defining optical property'},
                        {'interface': IFileStr, 'name': 'pattern', 'value': None, 'desc': 'file/file content that defines a domain to till the scene'},
                        {'interface': None, 'name': 'options', 'value': None, 'desc': 'dictionarry allowing to set user option.Available options are:\n        \n        1st: consider only direct projection if True.\n        Nz: number of layers to be consider for the scene\n        Hc: height of the can scene\n        Ds: diameter of the sphere for nested radiosity\n        debug : print messages and prevent removal of tempdir\n        resdir : store caribu results as files in resdir if resdir is not None, store nothing otherwise\n        wavelength: list of name to be used as keys for output dict (if None use the name of the opt files or the generic names band0,band1 if optfiles are given as content)'}],
                outputs=[{'interface': None, 'name': 'irradiances', 'desc': ''},
                         {'interface': None, 'name': 'Settings', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('caribu_vcaribu')


CaribuScene_nodes_generate_scene = Factory(name='generate scene',
                authors='C. Fournier, C Pradal',
                description='generate a PlantGL scene form a Caribu Scene',
                category='scene',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='generate_scene_node',
                inputs=[{'interface': None, 'name': 'CaribuScene'},
                        {'interface': IDict, 'name': 'colors', 'value': None}],
                outputs=[{'interface': None, 'name': 'PlantGL scene'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('CaribuScene_nodes_generate_scene')


reduceDict_reduceDict = Factory(name='reduceDict',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='apply dictionary reduction ',
                category='Unclassified',
                nodemodule='alinea.caribu.reduceDict',
                nodeclass='reduceDict',
                inputs=[{'interface': None, 'name': 'dictlist', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'reduceddict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('reduceDict_reduceDict')



label_decode_label = Factory(name='decode label',
                authors='C. Fournier',
                description='',
                category='io',
                nodemodule='alinea.caribu.label',
                nodeclass='decode_label',
                inputs=[{'interface': ISequence, 'name': 'canLabels'}],
                outputs=[{'interface': ISequence, 'name': 'optical species'},
                         {'interface': ISequence, 'name': 'Opacity'},
                         {'interface': ISequence, 'name': 'Plant id'},
                         {'interface': ISequence, 'name': 'Element id'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('label_decode_label')


filterby_filterby = Factory(name='filterby',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Return values whose indices match condition',
                category='Unclassified',
                nodemodule='alinea.caribu.filterby',
                nodeclass='filterby',
                inputs=[{'interface': ISequence, 'name': 'indices', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'values', 'value': None, 'desc': ''}, {'interface': IFunction, 'name': 'condition', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'values', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('filterby_filterby')



mtg_updateMTG = Factory(name='updateMTG',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='',
                category='data i/o',
                nodemodule='alinea.caribu.mtg',
                nodeclass='updateMTG',
                inputs=[{'interface': None, 'name': 'mtg', 'value': None, 'desc': ''}, {'interface': None, 'name': 'caribu output', 'value': None, 'desc': ''}, {'interface': None, 'name': 'mtg id for triangles', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'prefix for mtg property', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'updated mtg', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('mtg_updateMTG')



PARaggregators_PARaggregators = Factory(name='PARaggregators',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='returns a dict of aggregators (0/1) for summing Eabs at different levels',
                category='Unclassified',
                nodemodule='alinea.caribu.PARaggregators',
                nodeclass='PARaggregators',
                inputs=[{'interface': None, 'name': 'aggregation table', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'aggegators', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('PARaggregators_PARaggregators')







CaribuScene_nodes_WriteCan = Factory(name='WriteCan',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='',
                category='io',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='WriteCan',
                inputs=[{'interface': IInterface, 'name': 'CaribuScene', 'value': None, 'desc': ''}, {'interface': IFileStr, 'name': 'filename', 'value': None, 'desc': ''}],
                outputs=[{'interface': IFileStr, 'name': 'filename', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_WriteCan')










CaribuScene_nodes_addShapes = Factory(name='addShapes',
                authors='C. Fournier',
                description='',
                category='io',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='addShapes',
                inputs=[{'interface': None, 'name': 'CaribuScene', 'value': None, 'desc': ''}, {'interface': None, 'name': 'Shapes', 'value': None, 'desc': ''}, {'interface': None, 'name': 'Tesselator', 'value': None, 'desc': 'PlantGL tesselator instance or None'}, {'interface': None, 'name': 'CanLabels', 'value': None, 'desc': 'Labels used by Caribu to make the association between opticals properties and shapes '}, {'interface': IBool, 'name': 'auto generates Can labels', 'value': True, 'desc': 'uses opt=1 and opak = 0 for all primitives, see label encode for alternatives'}, {'interface': IBool, 'name': 'Copy Caribuscene', 'value': True, 'desc': 'uncheck only if you know what you do (pass by reference)'}],
                outputs=[{'interface': None, 'name': 'CaribuScene', 'desc': ''}, {'interface': IDict, 'name': 'Shape_id2Caribu_id', 'desc': 'mapping of shapes id to internal caribu id'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_addShapes')



mtg_to_canestra = Factory(name='MtgToCan',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Give a canestra repr of MTG',
                category='data i/o',
                nodemodule='alinea.caribu.mtg',
                nodeclass='to_canestra',
                inputs=[{'interface': None, 'name': 'MTG', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'Property to use as OptId', 'value': 'optical_specie', 'desc': ''}, {'interface': IStr, 'name': 'Property to use as opacity', 'value': 'transparency', 'desc': ''}, {'interface': IStr, 'name': 'Property to use as Geometry', 'value': 'geometry', 'desc': ''}, {'interface': IInt, 'name': 'Deault for optid', 'value': 1, 'desc': ''}, {'interface': IInt, 'name': 'Defalt for opacity', 'value': 0, 'desc': ''}, {'interface': IFloat(min=0, max=16777216, step=0.000001), 'name': 'minimal area', 'value': 1e-05, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'mtgId', 'desc': 'list of mtd id associated with triangles'}, {'interface': None, 'name': 'CanString', 'desc': 'Canestra input file'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('mtg_to_canestra')



label_encode_label = Factory(name='encode label',
                authors='C. Fournier',
                description='',
                category='io',
                nodemodule='alinea.caribu.label',
                nodeclass='encode_label',
                inputs=[{'interface': IInt, 'name': 'optical species', 'value': 1},
                        {'interface': IInt, 'name': 'Opacity', 'value': 1, 'desc': '0 means transparent(leaves), 1 means opak (stems)'},
                        {'interface': IInt, 'name': 'Plant id', 'value': 1},
                        {'interface': IInt, 'name': 'element id', 'value': 1},
                        {'interface': IInt, 'name': 'minimal length for the output', 'value': 1}],
                outputs=[{'interface': ISequence, 'name': 'canLabels', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('label_encode_label')





CaribuScene_nodes_periodise = Factory(name='Periodise',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Fit the scene within its pattern',
                category='scene',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='periodise',
                inputs=[{'interface': None, 'name': 'CaribuScene'}, {'interface': IBool, 'name': 'Copy Caribuscene', 'value': True, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'FittedCaribuScene'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_periodise')



mydict_mydict = Factory(name='mydict',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='debug dict',
                category='Unclassified',
                nodemodule='alinea.caribu.mydict',
                nodeclass='mydict',
                inputs=[{'interface': None, 'name': 'liste of tuple', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'dict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('mydict_mydict')



CaribuScene_nodes_addSoil = Factory(name='addSoil',
                authors='C. Fournier',
                description='',
                category='scene.ecophysiology',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='addSoil',
                inputs=[{'interface': IData, 'name': 'CaribuScene', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'altitude (z)', 'value': 0.0}, {'interface': IBool, 'name': 'Copy Caribuscene', 'value': True, 'desc': ''}],
                outputs=[{'interface': IData, 'name': 'CaribuScene', 'desc': ''}, {'interface': IDict, 'name': 'Soil_id2Caribu_id', 'desc': 'mapping of soil id to internal caribu id'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_addSoil')



CaribuScene_nodes_output_by_id = Factory(name='Output by id',
                authors='C. Fournier',
                description='',
                category='io',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='output_by_id',
                inputs=[{'interface': None, 'name': 'CaribuScene', 'value': None, 'desc': ''}, 
                {'interface': None, 'name': 'Caribu Outputs', 'value': None, 'desc': ''}, 
                {'interface': None, 'name': 'user_id -> caribu_id dict', 'value': None, 'desc': 'if given uses user id instead of caribu internal id as a key'}, 
                {'interface': None, 'name': '(caribu or user)_id -> group_id dict', 'value': None, 'desc': 'if given uses group id instead of caribu internal id as a key'}, 
                {'interface': IBool, 'name': 'aggregate', 'value': True, 'desc': 'should results (one per triangle) be aggregated by objects ?'}],
                outputs=[{'interface': IDict, 'name': 'Output dict', 'desc': 'keys:can_id,values = variable'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_output_by_id')




CaribuScene_nodes_getIncidentEnergy = Factory(name='getIncidentEnergy',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='',
                category='scene.light',
                nodemodule='alinea.caribu.CaribuScene_nodes',
                nodeclass='getIncidentEnergy',
                inputs=[{'interface': None, 'name': 'CaribuScene'}],
                outputs=[{'interface': IFloat, 'name': 'Qi', 'desc': 'incident light flux received on an horizontal surface (per scene unit area)'}, {'interface': IFloat, 'name': 'Qem', 'desc': 'sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)'}, {'interface': IFloat, 'name': 'Einc', 'desc': 'total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set'}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('CaribuScene_nodes_getIncidentEnergy')



selectOutput_selectOutput = Factory(name='selectOutput',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Select a variable in the output dictionnary of caribu',
                category='Unclassified',
                nodemodule='alinea.caribu.selectOutput',
                nodeclass='selectOutput',
                inputs=[{'interface': None, 'name': 'EnergyLabel', 'value': None, 'desc': ''}, {'interface': IEnumStr(enum=['Eabs', 'Einc', 'Ei', 'EincSup', 'EincInf', 'Area', 'Eabsm2', 'EiInf', 'EiSup', 'Opt', 'Opak', 'Plt', 'Elt', 'label']), 'name': 'variable', 'value': None, 'desc': 'Eabs is absorbed radiation, Einc is incident radiation on objects'}],
                outputs=[{'interface': None, 'name': 'selected output', 'desc': ''}, {'interface': None, 'name': 'key', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('selectOutput_selectOutput')


lightString_lightString = Factory(name='light string',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='return a string formated for caribu light input from radiance plus azimutal and zenital angles',
                category='Unclassified',
                nodemodule='alinea.caribu.lightString',
                nodeclass='lightString',
                inputs=[{'interface': IFloat, 'name': 'Radiance', 'value': 1, 'desc': ''}, {'interface': IFloat, 'name': 'Zenith angle (deg)', 'value': 0, 'desc': ''}, {'interface': IFloat, 'name': 'Azimuth angle (deg)', 'value': 46, 'desc': ''}],
                outputs=[{'interface': IStr, 'name': 'vector', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
# __all__.append('lightString_lightString')





exposition_rain_and_light = Factory(name='rain and light star',
                                    nodemodule = 'caribu_star',
                                    nodeclass = 'rain_and_light_star')
# __all__.append('exposition_rain_and_light')


# moved nodes

CaribuZenithPar = Factory(name='CaribuZenithPar',
                          description='This node is not functional. Use workflow/CaribuZenithPar instead',
                          nodemodule='alinea.caribu.moved_nodes',
                          nodeclass='CaribuZenithPar', category='Unclassified',
                          doc='', inputs=[
        {'desc': '', 'interface': IData, 'name': 'CanScene', 'value': None},
        {'desc': '', 'interface': ISequence, 'name': 'Pattern', 'value': None},
    {'desc': '', 'interface': IEnumStr, 'name': 'scene_unit', 'value': None}],
                          outputs=[{'desc': '', 'interface': None,
                                    'name': 'CaribuScene'},
                                   {'desc': '', 'interface': None,
                                    'name': 'CaribuOutDict'},
                                   {'desc': '', 'interface': None,
                                    'name': 'sceneid_to_caribu_id'}])
__all__.append('CaribuZenithPar')

CaribuZenithParSoil = Factory(name='CarribuZenithParSoil',
                          description='This node is not functional. Use workflow/CaribuZenithParSoil instead',
                          nodemodule='alinea.caribu.moved_nodes',
                          nodeclass='CaribuZenithPar', category='Unclassified',
                          doc='', inputs=[
        {'desc': '', 'interface': IData, 'name': 'CanScene', 'value': None},
        {'desc': '', 'interface': ISequence, 'name': 'Pattern', 'value': None},
    {'desc': '', 'interface': IEnumStr, 'name': 'scene_unit', 'value': None}],
                          outputs=[{'desc': '', 'interface': None,
                                    'name': 'CaribuScene'},
                                   {'desc': '', 'interface': None,
                                    'name': 'CaribuOutDict'},
                                   {'desc': '', 'interface': None,
                                    'name': 'sceneid_to_caribu_id'}])
__all__.append('CaribuZenithParSoil')