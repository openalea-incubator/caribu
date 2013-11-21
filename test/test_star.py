from alinea.caribu.caribu_star import *
from alinea.adel.astk_interface import AdelWheat
from alinea.astk.plant_interface import *


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