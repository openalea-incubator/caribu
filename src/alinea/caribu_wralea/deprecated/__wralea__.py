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
