from alinea.caribu.exposition import *
from alinea.adel.astk_interface import AdelWheat
from alinea.astk.plant_interface import *


def test_exposition():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    geom = g.property('geometry')
    rain_exposition, rain_fraction = exposed_surface(geom)
    light_exposition, light_fraction = exposed_surface(geom, '16')
    return rain_exposition, rain_fraction, light_exposition, light_fraction
 
def test_rain_and_light():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    rain_and_light(g)
    return g