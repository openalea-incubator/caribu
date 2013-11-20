from alinea.caribu.exposition import *
from alinea.adel.astk_interface import AdelWheat
from alinea.astk.plant_interface import *


def test_exposition():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    geom = g.property('geometry')
    rain_exposition = exposition(geom)
    light_exposition = exposition(geom, '16')
 
def test_rain_and_light():
    wheat = AdelWheat()
    g,_ = new_canopy(wheat, age=100)
    rain_and_light_expositions(g)
    return g