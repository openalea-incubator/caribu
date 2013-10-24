from alinea.caribu.CaribuScene import CaribuScene


def test_tutorial():
    """ test of simple call to caribu, as in visualea tutorial
    """
    scene = "../src/caribu/data/filterT.can"
    light  = "../src/caribu/data/zenith.light"
    pattern = "../src/caribu/data/filter.8"
    opt = "../src/caribu/data/par.opt"
    c_scene = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    output = c_scene.runCaribu(infinity=False)
    return(c_scene, output)
    
def test_getOptical():
    cs, out = test_tutorial()
    opts = cs.getOptical()
    #assert opts[0] == (0.1,0.05,0.1,0.05)
    return opts
    
def test_getNormals():
    cs, out = test_tutorial()
    norms = cs.getNormals()
    #assert opts[0] == (0.1,0.05,0.1,0.05)
    return norms
  
def test_getCenters():
    cs, out = test_tutorial()
    centers = cs.getCenters()
    return centers
