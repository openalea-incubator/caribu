from alinea.caribu.caribu_star import *
from alinea.adel.astk_interface import AdelWheat
from alinea.astk.plant_interface import *
from alinea.adel.data_samples import adel_one_leaf
from alinea.adel.mtg_interpreter import mtg_interpreter

def test_inclin():
    g = adel_one_leaf()
    # flaten the leaf
    blade = g.node(8)
    x,y,s,r = blade.shape_xysr
    y *= 0
    blade.shape_xysr = (x,y,s,r)
    stars = []
    for inclin in (0,0.5,1): #relative inclination compare to flat leaf
        blade.inclination = inclin
        mtg_interpreter(g)
        geom = g.property('geometry')
        star, exposed_area = caribu_star(geom)
        stars.append(star)
    return g, stars

def test_star():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    geom = g.property('geometry')
    rain_star, rain_exposed_area = caribu_star(geom)
    light_star, light_exposed_area = caribu_star(geom, '16')
    return rain_star, rain_exposed_area, light_star, light_exposed_area
 
def test_rain_and_light():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    rain_and_light_star(g)
    return g