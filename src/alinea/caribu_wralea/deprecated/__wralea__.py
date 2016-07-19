# This file has been generated at Sat Aug 04 18:13:50 2012

from openalea.core import *

__name__ = 'alinea.caribu.deprecated'

__editable__ = True
__description__ = ' Caribu package '
__license__ = ''
__url__ = ''
__version__ = '0.0.4'
__authors__ = 'M. Chelle,C. Fournier'
__institutes__ = 'INRA'

__all__ = []

CaribuScene_nodes_GenOutput = Factory(name='GenOutput',
                                      authors='M. Chelle,C. Fournier (wralea authors)',
                                      description='deprecated node',
                                      nodemodule='alinea.caribu.deprecated_nodes',
                                      nodeclass='GenOutput', inputs=[
        {'interface': IStr, 'name': 'Etri', 'value': None, 'desc': ''},
        {'interface': IStr, 'name': 'Eabs', 'value': None, 'desc': ''}],
                                      outputs=[
                                          {'interface': None, 'name': 'OutDict',
                                           'desc': ''}], widgetmodule=None,
                                      widgetclass=None)
__all__.append('CaribuScene_nodes_GenOutput')

CaribuScene_nodes_FileCaribuScene = Factory(name='FileCaribuScene',
                                               authors='C. Fournier',
                                               description='deprecated node',
                                               nodemodule='alinea.caribu.deprecated_nodes',
                                               nodeclass='FileCaribuScene',
                                               inputs=[{'interface': IFileStr(
                                                   filter="*.can", save=False),
                                                        'name': 'CanFile',
                                                        'value': None,
                                                        'desc': ''}, {
                                                           'interface': IFileStr(
                                                               filter="*.light",
                                                               save=False),
                                                           'name': 'LightFile',
                                                           'value': None,
                                                           'desc': ''}, {
                                                           'interface': IFileStr(
                                                               filter="*.8",
                                                               save=False),
                                                           'name': 'PatternFile',
                                                           'value': None,
                                                           'desc': ''}, {
                                                           'interface': IFileStr(
                                                               filter="*.opt",
                                                               save=False),
                                                           'name': 'OptFile',
                                                           'value': None,
                                                           'desc': ''}],
                                               outputs=[{'interface': IStr,
                                                         'name': 'CaribuScene',
                                                         'desc': ''},
                                                        {'interface': IDict,
                                                         'name': 'Maping dict (see CaribuScene)'}],
                                               widgetmodule=None,
                                               widgetclass=None, )
__all__.append('CaribuScene_nodes_FileCaribuScene')

CaribuScene_nodes_ObjCaribuScene = Factory(name='ObjCaribuScene',
                                              authors='M. Chelle,C. Fournier (wralea authors)',
                                              description='deprecated node',
                                              nodemodule='alinea.caribu.deprecated_nodes',
                                              nodeclass='ObjCaribuScene',
                                              inputs=[{'interface': IData,
                                                       'name': 'CanObj',
                                                       'value': None,
                                                       'desc': 'Canopy object with to_canestra method'},
                                                      {'interface': IStr,
                                                       'name': 'LightString',
                                                       'value': None,
                                                       'desc': ''},
                                                      {'interface': ISequence,
                                                       'name': 'pattern',
                                                       'value': None,
                                                       'desc': 'Tuple describig pattern'},
                                                      {'interface': IStr,
                                                       'name': 'optstring',
                                                       'value': None,
                                                       'desc': 'Optical properties'},
                                                      {'interface': IStr,
                                                       'name': 'wavelength',
                                                       'value': None,
                                                       'desc': 'Current wavelength'}],
                                              outputs=[{'interface': IStr,
                                                        'name': 'CaribuScene',
                                                        'desc': ''},
                                                       {'interface': IDict,
                                                        'name': 'Mapid',
                                                        'desc': ''}],
                                              widgetmodule=None,
                                              widgetclass=None, )
__all__.append('CaribuScene_nodes_ObjCaribuScene')

CaribuScene_nodes_getEi = Factory(name='get Ei',
                                  authors='M. Chelle,C. Fournier (wralea authors)',
                                  description='deprecated node',
                                  nodemodule='alinea.caribu.deprecated_nodes',
                                  nodeclass='getEi', inputs=[
        {'interface': None, 'name': 'CaribuScene'}], outputs=[
        {'interface': IFloat, 'name': 'Qi',
         'desc': 'incident light flux received on an horizontal surface (per scene unit area)'}],
                                  widgetmodule=None, widgetclass=None, )
__all__.append('CaribuScene_nodes_getEi')


MCSail_MCSail = Factory(name='MCSail',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Compute mean fluxes on layered canopy',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
                nodeclass='MCSail',
                inputs=[{'interface': None, 'name': 'Sailscene'},
                        {'interface': IBool, 'name': 'Sleep', 'value': False}],
                outputs=[{'interface': IStr, 'name': 'Fluxes'},
                         {'interface': IStr, 'name': 'Log'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('MCSail_MCSail')

S2v_S2v = Factory(name='S2v',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Transform a 3D CaribuScene into a 1D Sail Scene',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
                nodeclass='S2v',
                inputs=[{'interface': None, 'name': 'CaribuScene', 'value': None, 'desc': ''},
                        {'interface': IInt, 'name': 'Number of layers', 'value': 5, 'desc': ''},
                        {'interface': IFloat, 'name': 'ZmaxLayer', 'value': 2.0, 'desc': ''},
                        {'interface': IBool, 'name': 'Sleep', 'value': False, 'desc': ''}],
                outputs=[{'interface': IStr, 'name': 'SailScene', 'desc': ''},
                         {'interface': ISequence, 'name': 'TriangleLayerLabels', 'desc': ''}, {'interface': IStr, 'name': 'Log', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('S2v_S2v')

Canestra_Canestra = Factory(name='Canestra',
                authors='M. Chelle,C. Fournier (wralea authors)',
                description='Nested radiosity illumination of a 3D Scene ',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
                nodeclass='Canestra',
                inputs=[{'interface': None, 'name': 'CaribuScene', 'value': None, 'desc': ''},
                        {'interface': IStr, 'name': 'SailFluxes', 'value': None, 'desc': ''},
                        {'interface': IBool, 'name': 'No Multiple Scattering', 'value': True, 'desc': ''},
                        {'interface': IFloat, 'name': 'Sphere Diameter', 'value': 0.5, 'desc': ''},
                        {'interface': IBool, 'name': 'keep FF in Scene', 'value': False, 'desc': ''}],
                outputs=[{'interface': IStr, 'name': 'CaribuScene', 'desc': ''}, {'interface': IStr, 'name': 'Etri', 'desc': ''}, {'interface': IStr, 'name': 'Eabs', 'desc': ''}, {'interface': IStr, 'name': 'Log', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('Canestra_Canestra')

CaribuScene_nodes_addSoil = Factory(name='addSoil',
                authors='C. Fournier',
                description='',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
                nodeclass='addSoil',
                inputs=[{'interface': IData, 'name': 'CaribuScene', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'altitude (z)', 'value': 0.0}, {'interface': IBool, 'name': 'Copy Caribuscene', 'value': True, 'desc': ''}],
                outputs=[{'interface': IData, 'name': 'CaribuScene', 'desc': ''}, {'interface': IDict, 'name': 'Soil_id2Caribu_id', 'desc': 'mapping of soil id to internal caribu id'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('CaribuScene_nodes_addSoil')

CaribuScene_nodes_addShapes = Factory(name='addShapes',
                authors='C. Fournier',
                description='',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
                nodeclass='addShapes',
                inputs=[{'interface': None, 'name': 'CaribuScene', 'value': None, 'desc': ''},
                        {'interface': None, 'name': 'Shapes', 'value': None, 'desc': ''},
                        {'interface': None, 'name': 'Tesselator', 'value': None, 'desc': 'PlantGL tesselator instance or None'},
                        {'interface': None, 'name': 'CanLabels', 'value': None, 'desc': 'Labels used by Caribu to make the association between opticals properties and shapes '},
                        {'interface': IBool, 'name': 'auto generates Can labels', 'value': True, 'desc': 'uses opt=1 and opak = 0 for all primitives, see label encode for alternatives'},
                        {'interface': IBool, 'name': 'Copy Caribuscene', 'value': True, 'desc': 'uncheck only if you know what you do (pass by reference)'}],
                outputs=[{'interface': None, 'name': 'CaribuScene', 'desc': ''}, {'interface': IDict, 'name': 'Shape_id2Caribu_id', 'desc': 'mapping of shapes id to internal caribu id'}],
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('CaribuScene_nodes_addShapes')

CaribuScene_nodes_output_by_id = Factory(name='Output by id',
                authors='C. Fournier',
                description='',
                category='deprecated',
                nodemodule='alinea.caribu.deprecated_nodes',
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
__all__.append('CaribuScene_nodes_output_by_id')