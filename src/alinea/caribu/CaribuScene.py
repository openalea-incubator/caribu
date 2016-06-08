""" This module defines CaribuScene and CaribuSceneError classes."""

import os
from itertools import groupby, izip

from openalea.mtg.mtg import MTG
from openalea.plantgl.all import Scene as pglScene

from alinea.caribu.file_adaptor import read_can, read_light, read_pattern, read_opt, build_materials
from alinea.caribu.plantgl_adaptor import scene_to_cscene, mtg_to_cscene


def _agregate(values, indices, fun=sum):
    """ performs aggregation of outputs along indices """
    ag = {}
    for key, group in groupby(sorted(izip(indices, values), key=lambda x: x[0]), lambda x: x[0]):
        vals = [elt[1] for elt in group]
        try:
            ag[key] = fun(vals)
        except TypeError:
            ag[key] = vals[0]
    return ag


class CaribuScene(object):
    """A class interface to Caribu algorithms"""

    default_material = (0.06, 0.07)
    default_soil_reflectance = 0.15
    default_light = (1, (0, 0, -1))

    def __init__(self, scene=None, light=None, pattern=None, opt=None, soil_reflectance=None):
        """ Initialise a CaribuScene

        Args:
            scene: a {primitive_id: [triangles,]} dict.A triangle is a list of 3-tuples points coordinates
                    Alternatively, scene can be a *.can file or a mtg with 'geometry' property or a plantGL scene.
                    For the later case, primitive_id is taken as the index of the shape in the scene shape list.
            light: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining light sources
                    Alternatively,  a *.light file
                    If None (default), a unit energy vertical light is used.
            pattern: (tuple of floats) 2D Coordinates of the domain bounding the scene for its replication.
                     (xmin, ymin, xmax, ymax) scene is not bounded along z axis.
                     Alternatively a *.8 file.
                     if None (default), scene is not repeated
            opt: a {band_name: {primitive_id: material}} dict of dict.
                    A material is a 1-, 2- or 4-tuple depending on its optical behavior.
                    A 1-tuple encode an opaque material characterised by its reflectance
                    A 2-tuple encode a symmetric translucent material defined by a reflectance and a transmittance
                    A 4-tuple encode an asymmetric translucent material defined the reflectance and transmittance
                    of the upper and lower side respectively
                    Alternatively, a list of band_name.opt files (require scene to be given as a *.can file)
                    If None (default), all primitive are associated to the default material of the class.
            soil_reflectance: a {band_name: reflectance} dict.
                    If None (default) class default soil reflectance is used for all bands
                    If *.opt files are provided, the values in opt files is used in priority

        Returns:
            A CaribuScene instance

        Note:
            File format specifications (*.can, *.light, *.8, *.opt) can be found in data/CanestraDoc.pdf
        """

        # self.scene_labels = []  # list of external identifier/canlabel of each triangle present in the scene
        # self.scene_ids = []  # list of internal ids, as long as scene, used to aggegate outputs by primitive
        # self.colors = {}  # dict of id->(r,g,b) tuples of ambient colors of primitives
        # self.pid = 1  # internal pending id to be given to the next primitive

        self.scene = None
        if scene is not None:
            if isinstance(scene, dict):
                elt = scene[scene.keys()[0]]
                try:
                    assert isinstance(elt, list)
                    assert isinstance(elt[0], list)
                    assert isinstance(elt[0][0], tuple)
                except:
                    raise ValueError('Unrecognised scene format')
                self.scene = scene
            elif isinstance(scene, str):
                self.scene = read_can(scene)
            elif isinstance(scene, MTG):
                self.scene = mtg_to_cscene(scene)
            elif isinstance(scene, pglScene):
                self.scene = scene_to_cscene(scene)
            else:
                raise ValueError('Unrecognised scene format')

        self.light = self.default_light
        if light is not None:
            if isinstance(light, list):
                elt = light[0]
                try:
                    assert isinstance(elt, tuple)
                    assert isinstance(elt[1], tuple)
                except:
                    raise ValueError('Unrecognised light format')
                self.light = light
            elif isinstance(light, str):
                self.light = read_light(light)

        self.pattern = None
        if pattern is not None:
            if isinstance(pattern, tuple):
                if len(pattern) == 2:
                    pattern = sum(pattern, ())
                if len(pattern) != 4:
                    raise ValueError('Unrecognised pattern format')
                self.pattern = pattern
            elif isinstance(pattern, str):
                self.pattern = read_pattern(pattern)
            else:
                raise ValueError('Unrecognised pattern format')

        self.material = None
        if opt is None:
            if soil_reflectance is None:
                self.soil_reflectance = {'default_band': self.default_soil_reflectance}
                bands = ['default_band']
            else:
                self.soil_reflectance = soil_reflectance
                bands = soil_reflectance.keys()
            if scene is not None:
                self.material = {}
                for band in bands:
                    self.material[band] = {pid: self.default_material for pid in self.scene}
        else:
            if isinstance(opt, list):
                if not isinstance(opt[0], str):
                    raise ValueError('Unrecognised opt format')
                if not isinstance(scene, str):
                    raise ValueError('un-compatible inputs types: opt file and scene not a can file')
                if self.scene is not None:
                    self.material = {}
                    self.soil_reflectance = {}
                    for path in opt:
                        band = os.path.basename(path).split('.')[0]
                        n, ro_soil, po = read_opt(path)
                        self.material[band] = build_materials(self.scene.keys(), po, ro_soil)
                        self.soil_reflectance[band] = ro_soil
            elif isinstance(opt, dict):
                elt = opt[opt.keys()[0]]
                if not isinstance(elt, dict):
                    raise ValueError('Unrecognised opt format')
                self.material = opt
                if soil_reflectance is None:
                    self.soil_reflectance = {band: self.default_soil_reflectance for band in opt}
                else:
                    if isinstance(soil_reflectance, dict):
                        if not len(soil_reflectance) == len(opt):
                            raise ValueError(
                                'the number of bands for optical properties and soil reflectance should match')
                        self.soil_reflectance = soil_reflectance
                    else:
                        raise ValueError('Unrecognised soil_reflectance format')
            else:
                raise ValueError('Unrecognised opt format')

    # def addSoil(self, zsoil=0., color=(170, 85, 0)):
    #     """ Add Soil to Caribu scene. Soil dimension is taken from pattern.
    #     zsoil specifies the heigth of the soil
    #
    #     """
    #     import string
    #     def _canString(ind, pts, label):
    #         s = "p 1 %s 3 %s" % (str(label), ' '.join('%.6f' % x for i in ind for x in pts[i]))
    #         return s + '\n'
    #
    #     ids = []
    #
    #     if not self.hasPattern:
    #         print('addSoil needs a pattern to be set')
    #
    #     else:
    #         pat = self.pattern
    #         xy = map(string.split, pat.splitlines())
    #         A = map(float, xy[0])
    #         C = map(float, xy[1])
    #         if (A[0] > C[0]):
    #             A = map(float, xy[1])
    #             C = map(float, xy[0])
    #         if (C[1] < A[1]):
    #             D = [A[0], C[1]]
    #             B = [C[0], A[1]]
    #         else:
    #             B = [A[0], C[1]]
    #             D = [C[0], A[1]]
    #         A.append(zsoil)
    #         B.append(zsoil)
    #         C.append(zsoil)
    #         D.append(zsoil)
    #
    #         label = ["000000000000", "000000000001"]
    #         canstring = "\n".join(
    #             [_canString(range(3), (A, B, C), label[0]), _canString(range(3), (C, D, A), label[1])])
    #         ids = [self.pid, self.pid + 1]
    #
    #         self.scene += canstring
    #         self.scene_ids.extend(ids)
    #         self.scene_labels.extend(label)
    #         self.colors[self.pid] = color
    #         self.colors[self.pid + 1] = color
    #         self.hasScene = True
    #         self.pid += 2
    #
    #     return dict(zip(label, ids))


    # def generate_scene(self, colors=None):
    #     """
    #     Generate PlantGL scene from Caribu scene
    #
    #     Colors is an (optional) list of (rgb) tuples specifiying colors of individual triangles in the scene
    #
    #     """
    #     scene = pgl.Scene()
    #
    #     if len(self.scene_ids) > 0:  # scene is not empty
    #
    #         triangles = self.getTriangles()
    #
    #         geoms = {}
    #
    #         for i, triangle in enumerate(triangles):
    #             id = self.scene_ids[i]
    #             if id not in geoms:
    #                 geoms[id] = pgl.TriangleSet([], [])
    #                 if colors:
    #                     geoms[id].colorList = []
    #                     geoms[id].colorPerVertex = False
    #             shape = geoms[id]
    #             count = len(shape.pointList)
    #             shape.pointList.append(triangle[0])
    #             shape.pointList.append(triangle[1])
    #             shape.pointList.append(triangle[2])
    #             shape.indexList.append(pgl.Index3(count, count + 1, count + 2))
    #             if colors:
    #                 r, g, b = colors[i]
    #                 shape.colorList.append(pgl.Color4(r, g, b, 0))
    #
    #         for id, geom in geoms.iteritems():
    #             if colors:
    #                 shape = geom
    #                 shape.id = id
    #             else:
    #                 material = pgl.Material(pgl.Color3(*self.colors[id]))
    #                 shape = pgl.Shape(geom, material)
    #                 shape.id = id
    #
    #             scene += shape
    #
    #     return (scene)
    #
    # def plot(self, output, what='Eabsm2', minval=None, maxval=None):
    #     eabs = output[what]
    #     if minval is None:
    #         minval = min(eabs)
    #     if maxval is None:
    #         maxval = max(eabs)
    #     cmap = ColorMap()
    #     colors = map(lambda x: cmap(x, minval, maxval, 250., 20.), eabs)
    #     scene = self.generate_scene(colors)
    #     pgl.Viewer.display(scene)
    #     return scene
    #
    #
    #
    # def getIncidentEnergy(self):
    #     """ Compute Qi, Qem, Einc on the scene given current light sources.
    #
    #     Qi is the incident light flux received on an horizontal surface (per scene unit area)
    #     Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
    #     Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set
    #
    #     """
    #     import numpy
    #     Qi, Qem, Einc = None, None, None
    #
    #     if self.hasSources:
    #         sources = self.sources_as_array()
    #
    #         Qi = sources.energy.sum()
    #
    #         # costheta = k . direction, k etant le vecteur (0,0,1) et theta l'angle avec la verticale = abs(zdirection) / norm(direction)
    #         norm = numpy.sqrt(sources.vx ** 2 + sources.vy ** 2 + sources.vz ** 2)
    #         costheta = abs(sources.vz) / norm
    #         Qem = (sources.energy / costheta).sum()
    #
    #         if self.hasPattern:
    #             domain = self.pattern_as_array()
    #             d_area = abs(numpy.diff(domain.x) * numpy.diff(domain.y))[0]
    #             Einc = Qi * d_area
    #
    #     return Qi, Qem, Einc
    #
    # def getOptical(self):
    #     """ return a list of tuple (reflectance, transmitance) for all triangles in the scene
    #     """
    #     from label import Label
    #     def _reftrans(label, po):
    #         if label.is_soil():
    #             res = (po['albedo'], 0, 0, 0)
    #         else:
    #             esp = label.optical_id
    #             opts = po['species'][esp]
    #             if label.is_stem():
    #                 res = (opts[0], 0, 0, 0)
    #             else:
    #                 res = (opts[1:])
    #         return res
    #
    #     labels = map(Label, self.scene_labels)
    #     # pase opt (in getPO)
    #     # self.PO.splitlines()
    #     po = {'albedo': 0.2, 'species': {1: (10, 1, 1, 1, 1), 2: (20, 2, 2, 2, 2)}}
    #     return [_reftrans(lab, po) for lab in labels]
    #
    # def getTriangles(self):
    #     """ return a list of  triangles in the scene
    #     """
    #     canstring = self.scene
    #     return [res for res in (_get_triangle(x) for x in canstring.splitlines()) if res]
    #
    # def getAreas(self):
    #     """ return a list of areas for all triangles in the scene
    #     """
    #
    #     def _surf(triangle):
    #         A, B, C = triangle
    #         return pgl.norm(pgl.cross(B - A, C - A)) / 2.0
    #
    #     triangles = self.getTriangles()
    #     return [_surf(tri) for tri in triangles]
    #
    # def getNormals(self):
    #     """ return a list of normals (as pgl.vector3) for all triangles in the scene
    #     """
    #     from openalea.plantgl.all import cross
    #     def _normal(triangle):
    #         A, B, C = triangle
    #         n = cross(B - A, C - A)
    #         return n.normed()
    #
    #     triangles = self.getTriangles()
    #     return [_normal(tri) for tri in triangles]
    #
    # def getCenters(self):
    #     """ return a list of center coordinates for all triangles in the scene
    #     """
    #
    #     def _center(triangle):
    #         A, B, C = triangle
    #         return (A + B + C) / 3.
    #
    #     triangles = self.getTriangles()
    #     return [_center(tri) for tri in triangles]



    def get_caribu_output(self, vcdict):
        """ Get, filter and arrange output of caribu for use in CaribuScene. """

        from itertools import izip

        def _nan_to_zero(x):
            try:
                from math import isnan
            except:
                # to be back compatile with python 2.5
                def isnan(num):
                    return num != num
            return (0 if isnan(x) else x)

        d = vcdict[vcdict.keys()[0]]['data']
        # compute max value = sum of emmission of sources
        # _,eimax,_ = self.getIncidentEnergy()
        for k in ('Ei_inf', 'Ei_sup', 'Eabs'):
            d[k] = map(_nan_to_zero, d[k])
            # filter negative values occuring in EiInf/EiSup
            d[k] = map(lambda (x): max(0, x), d[k])
        eabs = [e * a for e, a in izip(d['Eabs'], d['area'])]
        einc = [(esup + einf) * a for esup, einf, a in izip(d['Ei_sup'], d['Ei_inf'], d['area'])]
        ei = [esup + einf for esup, einf in izip(d['Ei_sup'], d['Ei_inf'])]
        eincsup = [esup * a for esup, a in izip(d['Ei_sup'], d['area'])]
        eincinf = [einf * a for einf, a in izip(d['Ei_inf'], d['area'])]

        csdict = {'Eabs': eabs, 'Einc': einc, 'Ei': ei, 'EincSup': eincsup, 'EincInf': eincinf,
                  'Area': d['area'],
                  'Eabsm2': d['Eabs'], 'EiInf': d['Ei_inf'], 'EiSup': d['Ei_sup'],
                  'label': d['label']}
        return csdict

    # def runCaribu(self, direct=True, nz=10, dz=5, ds=0.5, infinity=True, projection_image_size=1536):
    #     """ Call Caribu and return results"""
    #
    #     output = {}
    #     if len(self.scene_ids) > 0:  # scene is not empty
    #         from alinea.caribu.caribu_shell import vcaribu
    #         scene = None
    #         lightsources = None
    #         pattern = None
    #         if self.hasScene:
    #             scene = self.scene
    #         if self.hasSources:
    #             lightsources = self.sources
    #         opticals = self.PO
    #         if self.hasPattern:
    #             pattern = self.pattern
    #         optiondict = {'1st': direct, 'Nz': nz, 'Hc': dz, 'Ds': ds, 'infinity': infinity,
    #                       'wavelength': self.wavelength, 'projection_image_size': projection_image_size}
    #
    #         vcout, status = vcaribu(scene, lightsources, opticals, pattern, optiondict)
    #         output = self.get_caribu_output(vcout)
    #
    #     return (output)
    #
    # def runPeriodise(self):
    #     """ Call periodise and modify position of triangle in the scene to fit inside pattern"""
    #     if len(self.scene_ids) > 0:  # scene is not empty
    #         from alinea.caribu.caribu_shell import vperiodise
    #         scene = None
    #         pattern = None
    #         if self.hasScene:
    #             scene = self.scene
    #         if self.hasPattern:
    #             pattern = self.pattern
    #         newscene = vperiodise(scene, pattern)
    #         self.scene = newscene

    # def output_by_id(self, output, mapid=None, groups=None, aggregate=True):
    #     """ Return caribu outputs grouped or aggregated by ids
    #     mapid: a dict of external_id -> caribu internal id. If given, the results are given for external _ids
    #     groups : a dict of id (internal of external) -> group_id. If given, results are computed for each group_id. Keys in groups are expected to be internal id if mapid is none, or external ids if mapid is given.
    #     if aggregate is True, one scalar is return by id (sum or weighted mean), otherwise it returns the list of values of all triangles of the id.
    #
    #
    #     """
    #     import numpy
    #     #
    #     # + une fonction input_by_id qui renverrai hmin, hmax, h, normale, azimuth, area et lai pour differents aggregateurs
    #     res = {}
    #     if len(output) > 0:
    #         indices = self.scene_ids
    #
    #         if len(indices) != len(next(output.itervalues())):
    #             # caribu/periodise have filtered 0 areas triangle
    #             areas = self.getAreas()
    #             indices = numpy.array(indices)[numpy.array(areas) > 0]
    #             if len(indices) != len(next(output.itervalues())):
    #                 # tries (exprerimental and limited to 10 mismatchs) to match input/output values based on area comparison
    #                 print "caribu: Warning : there is a mismatch between input and output, try to repair..."
    #                 in_areas = numpy.array(areas)[numpy.array(areas) > 0]
    #                 out_areas = numpy.array(output['Area'])
    #                 tried = 0
    #                 while ((len(in_areas) != len(out_areas)) and tried < 10):
    #                     tried += 1
    #                     isel = numpy.arange(len(out_areas))
    #                     r = in_areas[isel] / out_areas[isel]
    #                     notclose = numpy.invert(numpy.isclose(r, numpy.ones(len(out_areas)), 1e-2))
    #                     if not any(notclose):  # mismatch is for triangle at the end of in_areas
    #                         delindex = max(isel) + 1
    #                     else:
    #                         delindex = min(isel[notclose])
    #                     indices = numpy.delete(indices, delindex)
    #                     in_areas = numpy.delete(in_areas, delindex)
    #             if len(indices) != len(next(output.itervalues())):
    #                 raise CaribuSceneError(
    #                     "Caribu outputs can't be aggregated due to a mismatch between the number of input triangles (%d) and the number of output values(%d)" % (
    #                         len(indices), len(next(output.itervalues()))))
    #
    #         if groups:
    #             new_map = {}  # dict of group_id -> reference internal id (reference id is the first one found belonging to a group)
    #             aliases = {}  # dict of internal_id -> reference id of a group
    #             for id in groups:
    #                 gid = groups[id]
    #                 if mapid:
    #                     id = mapid[id]
    #                 if gid in new_map:
    #                     aliases[id] = new_map[gid]
    #                 else:
    #                     new_map[gid] = id
    #             mapid = new_map
    #             indices = [aliases[id] if id in aliases else id for id in indices]
    #
    #         # aggregation uses internal ids as unicity of scene_labels is not guarantee (eg if several scenes have been mixed)
    #         if aggregate:
    #             # compute sums for area integrated variables
    #             res = dict([(k, _agregate(output[k], indices)) for k in
    #                         ['Eabs', 'Einc', 'EincSup', 'EincInf', 'Area', 'label']])
    #             # compute mean fluxes
    #             res['Eabsm2'] = dict([(k, res['Eabs'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k, 0) for k in
    #                                   res['Eabs'].iterkeys()])
    #             res['Ei'] = dict(
    #                 [(k, (res['EincInf'][k] + res['EincSup'][k]) / res['Area'][k]) if res['Area'][k] > 0 else (k, 0) for
    #                  k in res['EincInf'].iterkeys()])
    #             res['EiInf'] = dict([(k, res['EincInf'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k, 0) for k in
    #                                  res['EincInf'].iterkeys()])
    #             res['EiSup'] = dict([(k, res['EincSup'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k, 0) for k in
    #                                  res['EincSup'].iterkeys()])
    #         else:
    #             res = dict([(k, _agregate(output[k], indices, list)) for k in output.keys()])
    #
    #         # re-index results if mapid is given
    #         if mapid is not None:  # empty mapid (corrresponding to absence of a list of shapes in the scene) should pass this test. Only none default options should skip and return all res
    #             for var in res.keys():
    #                 res[var] = dict([(k, (res[var]).get(v, numpy.nan)) for k, v in mapid.items()])
    #             if len(res[res.keys()[0]]) <= 0:  # pas de res trouve pour les mapid en entree
    #                 res = {}
    #
    #     return (res)
