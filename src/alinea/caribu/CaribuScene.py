# -*- python -*-
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       WebSite : https://github.com/openalea-incubator/caribu
#
# ==============================================================================
""" This module defines CaribuScene and CaribuSceneError classes."""

import os
from itertools import groupby, izip, chain

from openalea.mtg.mtg import MTG
from openalea.plantgl.all import Scene as pglScene, Viewer

from alinea.caribu.file_adaptor import read_can, read_light, read_pattern, read_opt, build_materials
from alinea.caribu.plantgl_adaptor import scene_to_cscene, mtg_to_cscene
from alinea.caribu.caribu import raycasting, radiosity, mixed_radiosity, x_raycasting, x_radiosity, x_mixed_radiosity
from alinea.caribu.display import jet_colors, generate_scene


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


def _convert(output, conv_unit):
    """ convert caribu output to meter/meter_square
    """
    # To DO ? filtering eabs_max / zero + occultations ?
    if conv_unit == 1:
        return output
    else:
        meter_square = conv_unit ** 2
        output['area'] = [area * meter_square for area in output['area']]
        for k in ['Eabs', 'Ei', 'Ei_sup', 'Ei_inf']:
            output[k] = [nrj / meter_square for nrj in output[k]]
        return output


def _wsum(nrj_area):
    nrj, area = zip(*nrj_area)
    area_tot = sum(area)
    if area_tot == 0:
        return 0
    else:
        return sum([e * a if a > 0 else 0 for e, a in nrj_area]) / area_tot


def domain_mesh(domain, z=0., subdiv=1):
    """ Create a triangle mesh covering a domain at height z

    Args:
        domain: (tuple of float) : a (xmin, ymin, xmax, ymax) tuple defining the extend of a square domain
        z: the altitude of the mesh
        subdiv: the number of subdivision of the mesh (not functional)

    Returns:
        a list of triangles. A triangle is a list of 3-tuples points coordinates
    """

    xmin, ymin, xmax, ymax = domain

    if subdiv > 1:
        raise UserWarning('subdivision of mesh not yet implemented')
        # TODO: copy code from cpp/canopy_io.cpp, function parse_can
    a = (xmin, ymin, z)
    b = (xmax, ymin, z)
    c = (xmin, ymax, z)
    d = (xmax, ymax, z)

    return [(a, b, c), (b, d, c)]


class CaribuScene(object):
    """A class interface to Caribu algorithms"""

    default_material = (0.06, 0.07)
    default_soil_reflectance = 0.15
    default_light = (1, (0, 0, -1))
    default_band = 'default_band'
    units = {'mm': 0.001, 'cm': 0.01, 'dm': 0.1, 'm': 1, 'dam': 10, 'hm': 100, 'km': 1000}

    def __init__(self, scene=None, light=None, pattern=None, opt=None, soil_reflectance=None, soil_mesh=None, z_soil=None,
                 scene_unit='m'):
        """ Initialise a CaribuScene

        Args:
            scene: a {primitive_id: [triangles,]} dict.A triangle is a list of 3-tuples points coordinates
                    Alternatively, scene can be a *.can file or a mtg with 'geometry' property or a plantGL scene.
                    For the later case, primitive_id is taken as the index of the shape in the scene shape list.
            light: (list of tuples) a list of (Energy, (vx, vy, vz)) tuples defining light sources
                    Alternatively,  a *.light file
                    If None (default), a unit energy vertical light is used.
                    Energy unit should be given per square-meter (m-2)
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
                    If *.opt files are provided, the values in opt files are used in priority
            soil_mesh: (int) a flag triggering for the creation of a soil mesh in the scene during computations
                    If None (default), no soil is added
                    If an int (n), a soil is added to the scene, with n subdivisions
            z_soil: (float) the altitude of the soil.
                    If None (default), the soil is placed at the bottom of the scene bounding box
            scene_unit (str): the unit of length used for scene coordinate and for pattern
                    (should be one of class.units default)
                    By default, scene_unit is considered to be 'm' (meter).

        Returns:
            A CaribuScene instance

        Note:
            File format specifications (*.can, *.light, *.8, *.opt) can be found in data/CanestraDoc.pdf
        """

        if scene_unit not in self.units:
            raise ValueError('unrecognised scene unit: ' + scene_unit)
        self.conv_unit = self.units[scene_unit]

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

        self.light = [self.default_light]
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
            else:
                raise ValueError('Unrecognised light format')

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
                self.soil_reflectance = {self.default_band: self.default_soil_reflectance}
                bands = [self.default_band]
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

        self.soil = None
        if soil_mesh is not None:
            if self.pattern is None:
                raise ValueError('Adding a soil needs the scene domain to be defined')
            if z_soil is None:
                if self.scene is None:
                    z_soil = 0
                else:
                    triangles = reduce(lambda x, y: x + y, self.scene.values())
                    z = (pt[2] for tri in triangles for pt in tri)
                    z_soil = min(z)
            self.soil = domain_mesh(self.pattern, z_soil, soil_mesh)

    def plot(self, a_property=None, minval=None, maxval=None, display=True):
        """

        Args:
            a_property: {dict of float or dict of list of float} : a dict of values,
                each key being a scene primitive index.
            minval: (float) minimal value at lower bound of color range
                    if None (default), minimal value of property is used
            maxval: (float) maximal value at upper bound of color range
                    if None (default), maximal value of property is used
            display: (bool) : should the scene be displayed ? (default True)

        Returns:
            A plantGL scene
        """
        if a_property is None:
            colors = None
            soil_colors = None
        else:
            values = a_property.values()
            if isinstance(values[0], list):
                values = list(chain.from_iterable(values))
            if minval is None:
                minval = min(values)
            if maxval is None:
                maxval = max(values)
            colors = {k: jet_colors(values, minval, maxval) for k in a_property}
        scene = generate_scene(self.scene, colors)
        if display:
            Viewer.display(scene)
        return scene

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



    def run(self, direct=True, infinite=False, d_sphere=0.5, layers=10, height=None, screen_size=1536,
            split_face=False, simplify=False):
        """ Compute illumination using the appropriate caribu algorithm

        Args:
            direct: (bool) Whether only first order interception is to be computed
                    Default is True (no rediffusions)
            infinite: (bool) Whether the scene should be considered as infinite
                    Default is False (non infinite canopy)
            d_sphere: (float) the diameter (m) of the sphere defining the close neighbourhood
                    of mixed radiosity algorithm
                       if d_sphere = 0, direct + pure layer algorithm is used
            layers: (int) the number of horizontal layers for estimating far contributions
            height: (float) the height of the canopy (m).
                    if None (default), the maximal height of the scene is used.
            screen_size: (int) buffer size for projection images (pixels)
            split_face: (bool) Whether results of incidence on individual faces of triangle should be outputed
                    Default is False
            simplify: (bool)  Whether results per band should be simplified to a {result_name: property} dict
                    in the case of a monochromatic simulation

        Returns:
            - raw (dict of dict) a {band_name: {result_name: property}} dict of dict.
            Each property is a {primitive_id: [values,]} dict containing results for individual triangles of the primitive
            - aggregated (dict of dict) : a {band_name: {result_name: property}}
            Each property is a {primitive_id: value} dict containing aggregated results for each primitive
            result_name are :
                      - area (float): the individual areas (m2)
                      - Eabs (float): the surfacic density of energy absorbed (m-2)
                      - Ei (float): the surfacic density of energy incoming  (m-2)
                      additionally, if split_face is True:
                      - Ei_inf (float): the surfacic density of energy incoming on the inferior face (m-2)
                      - Ei_sup (float): the surfacic density of energy incoming on the superior face (m-2)
        """

        raw, aggregated = {}, {}
        self.soil_raw, self.soil_aggregated = {}, {}
        results = ['Eabs', 'Ei', 'area']
        if split_face:
            results.extend(['Ei_inf', 'Ei_sup'])

        # convert lights to scene_unit
        lights = self.light
        if self.conv_unit != 1:
            lights = [(e * self.conv_unit ** 2, vect) for e, vect in self.light]

        if self.scene is not None:
            triangles = reduce(lambda x, y: x + y, self.scene.values())
            groups = [[pid] * len(self.scene[pid]) for pid in self.scene]
            groups = reduce(lambda x, y: x + y, groups)
            if self.soil is not None:
                triangles += self.soil
                groups = groups + ['soil'] * len(self.soil)
            bands = self.material.keys()
            if len(bands) == 1:
                materials = [[self.material[bands[0]][pid]] * len(self.scene[pid]) for pid in self.scene]
                materials = reduce(lambda x, y: x + y, materials)
                albedo = self.soil_reflectance[bands[0]]
                if self.soil is not None:
                    materials = materials + [(albedo,)] * len(self.soil)
                algos = {'raycasting': raycasting, 'radiosity': radiosity, 'mixed_radiosity': mixed_radiosity}
            else:
                materials = {}
                for band in bands:
                    mat = [[self.material[band][pid]] * len(self.scene[pid]) for pid in self.scene]
                    materials[band] = reduce(lambda x, y: x + y, mat)
                    if self.soil is not None:
                        materials = materials + [(self.soil_reflectance[band],)] * len(self.soil)
                albedo = self.soil_reflectance
                algos = {'raycasting': x_raycasting, 'radiosity': x_radiosity, 'mixed_radiosity': x_mixed_radiosity}

            if not direct and infinite:  # mixed radiosity will be used
                if d_sphere < 0:
                    raise ValueError('calling radiosity should be done using direct=False and infinite=False')
                d_sphere /= self.conv_unit
                if height is None:
                    z = (pt[2] for tri in triangles for pt in tri)
                    height = max(z)
                else:
                    height /= self.conv_unit

            if infinite and self.pattern is None:
                raise ValueError('infinite canopy illumination needs a pattern to be defined')

            if not direct and infinite:  # mixed radiosity
                out = algos['mixed_radiosity'](triangles, materials, lights=lights, domain=self.pattern,
                                               soil_reflectance=albedo,
                                               diameter=d_sphere, layers=layers, height=height, screen_size=screen_size)
            elif not direct:  # pure radiosity
                out = algos['radiosity'](triangles, materials, lights=lights, screen_size=screen_size)
            else:  # ray_casting
                if infinite:
                    out = algos['raycasting'](triangles, materials, lights=lights, domain=self.pattern,
                                              screen_size=screen_size)
                else:
                    out = algos['raycasting'](triangles, materials, lights=lights, domain=None, screen_size=screen_size)

            if len(bands) == 1:
                out = {bands[0]: out}
            for band in bands:
                output = _convert(out[band], self.conv_unit)
                raw[band] = {}
                aggregated[band] = {}
                for k in results:
                    raw[band][k] = _agregate(output[k], groups, list)
                    if k is 'area':
                        aggregated[band][k] = _agregate(output[k], groups, sum)
                    else:
                        aggregated[band][k] = _agregate(izip(output[k], output['area']), groups, _wsum)
                if self.soil is not None:
                    self.soil_raw[band] = {k: raw[band][k].pop('soil') for k in results}
                    self.soil_aggregated[band] = {k: aggregated[band][k].pop('soil') for k in results}


            if simplify and len(bands) == 1:
                raw = raw[bands[0]]
                aggregated = aggregated[bands[0]]

        return raw, aggregated

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
