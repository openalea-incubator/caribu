run_test = True
try:
    import openalea.plantgl.all as pgl
except ImportError:
    run_test = False

if run_test:
    import openalea.plantgl.all as pgl
    from alinea.caribu.CaribuScene import CaribuScene
    from alinea.caribu.data_samples import data_path


    def test_instantiation_from_files():
        can = str(data_path('filterT.can'))
        sky = str(data_path('Turtle16soc.light'))
        opts = map(str, [data_path('par.opt'), data_path('nir.opt')])
        pattern = str(data_path('filter.8'))

        # defaults
        cs = CaribuScene()
        assert cs.scene is None
        assert cs.light == [cs.default_light]
        assert cs.pattern is None
        assert cs.material is None
        assert cs.soil_reflectance[cs.default_band] == cs.default_soil_reflectance

        # complete set of files
        cs = CaribuScene(scene=can, light=sky, opt=opts, pattern=pattern)
        assert len(cs.scene) == 1
        assert len(cs.scene[cs.scene.keys()[0]]) == 192
        assert len(cs.light) == 16
        for band in ('nir', 'par'):
            assert band in cs.material
            assert len(cs.material[band]) == len(cs.scene)
        assert cs.soil_reflectance['par'] != cs.soil_reflectance['nir']
        assert len(cs.pattern) == 4

        # incomplete set of files
        cs = CaribuScene(scene=can)
        assert len(cs.material[cs.default_band]) == len(cs.scene)

        return cs


    def test_instantiation_from_python():
        s = pgl.Scene()
        s.add(pgl.Sphere())
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        triangles = [points]
        pyscene = {'t1': triangles}
        sky = [(0, (0, 0, -1)), (1, (0, 0, -1))]
        pattern = (0, 0, 20, 20)
        pattern_old_style = ((0, 0), (20, 20))
        materials = {'par': {'t1': (0.3,)}}
        soil_reflectance = {'par': 0}

        cs = CaribuScene(scene=s, light=sky, pattern=pattern)
        assert len(cs.scene) == 1
        assert len(cs.scene[0]) == 112
        assert len(cs.light) == 2
        assert len(cs.pattern) == 4
        assert cs.material[cs.default_band][0] == cs.default_material
        assert cs.soil_reflectance[cs.default_band] == cs.default_soil_reflectance

        cs = CaribuScene(scene=pyscene, opt=materials, pattern=pattern_old_style)
        assert len(cs.scene) == 1
        assert len(cs.scene['t1']) == 1
        assert cs.material == materials
        assert cs.soil_reflectance['par'] == cs.default_soil_reflectance
        assert len(cs.pattern) == 4

        cs = CaribuScene(scene=pyscene, soil_reflectance=soil_reflectance)
        assert 'par' in cs.material
        assert cs.soil_reflectance == soil_reflectance

        cs = CaribuScene(scene=pyscene, opt=materials, soil_reflectance=soil_reflectance)
        assert 'par' in cs.material
        assert cs.soil_reflectance == soil_reflectance

        return cs


    def test_run_monochrome():
        pts_1 = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        pts_2 = [(0, 0, 1e-5), (1, 0, 1e-5), (0, 1, 1e-5)]
        pts_3 = [(1, 0, 0), (1, 1, 0), (0, 1, 0)]
        pyscene = {'lower': [pts_1, pts_3], 'upper': [pts_2]}
        domain = (0, 0, 1, 1)
        cscene = CaribuScene(pyscene, pattern=domain)

        # raycasting
        out = cscene.run(direct=True, infinite=False)
        assert len(out) == 1
        assert len(out[cscene.default_band]['Eabs']) == 2
        assert len(out[cscene.default_band]['Eabs']['lower']) == 2
        assert len(out[cscene.default_band]['Eabs']['upper']) == 1

        # radiosity
        out = cscene.run(direct=False, infinite=False)
        assert len(out) == 1
        assert len(out[cscene.default_band]['Eabs']) == 2
        assert len(out[cscene.default_band]['Eabs']['lower']) == 2
        assert len(out[cscene.default_band]['Eabs']['upper']) == 1

        # mixed radiosity
        out = cscene.run(direct=False, infinite=True)
        assert len(out) == 1
        assert len(out[cscene.default_band]['Eabs']) == 2
        assert len(out[cscene.default_band]['Eabs']['lower']) == 2
        assert len(out[cscene.default_band]['Eabs']['upper']) == 1

        return out
