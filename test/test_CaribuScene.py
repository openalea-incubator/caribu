from alinea.caribu.CaribuScene import CaribuScene
import os

def test_tutorial():
    """ test of simple call to caribu, as in visualea tutorial
    """
    scene = "../src/caribu/data/f331s1_100plantes.can"
    light  = "../src/caribu/data/zenith.light"
    pattern = "../src/caribu/data/filter.8"
    opt="../src/caribu/data/opt/"
    resultatWaveL = {}
    for i in os.listdir(opt):
        if len(os.path.basename(opt+i).split('.')[1]) <= 3:
            c_scene = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt+i)
            output = c_scene.runCaribu(infinity=True)
            resultatWaveL[os.path.basename(opt+i).split('.')[0]] = output
    return(c_scene, resultatWaveL)
    
def test_tutorialBeta():
    """ test of simple call to caribu, as in visualea tutorial
    """
    scene = "../src/caribu/data/f331s1_100plantes.can"
    light  = "../src/caribu/data/zenith.light"
    pattern = "../src/caribu/data/filter.8"
    opt = "../src/caribu/data/par.opt"
    c_scene = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    output = c_scene.runCaribu(infinity=True)
    return(c_scene, output)

def test_getOptical():
    cs, out = test_tutorialBeta()
    opts = cs.getOptical()
   # assert opts[0] == (0.1,0.05,0.1,0.05)
    return opts
    
def test_getNormals():
    cs, out = test_tutorialBeta()
    norms = cs.getNormals()
    #assert opts[0] == (0.1,0.05,0.1,0.05)
    return norms
  
def test_getCenters():
    cs, out = test_tutorialBeta()
    centers = cs.getCenters()
    return centers
    