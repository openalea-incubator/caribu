from alinea.caribu.CaribuScene import CaribuScene
from alinea.caribu.data_samples import data_path

import openalea.plantgl.all as pgl

if __name__ == "__main__":
    print("--- test soilmesh")

    # Scene in Caribu format
    points = [(0.1, 0.1, 0.1), (0.1, 2, 0.1), (2, 2, 1), (2, 0.1, 1)]  
    triangles = {888 : [[points[0], points[1], points[2]], [points[0], points[2], points[3]]]}

    # environment parameters
    debug = False
    sky = data_path('zenith.light')
    opts = {'par' : {888 : (0.10, 0.05)}}
    domain = ((0, 0), (2,2))

    # radiosity
    c_scene = CaribuScene(scene=triangles, light=sky, opt=opts, soil_mesh = 1, debug = debug, pattern=domain)
    raw, aggregated = c_scene.run(direct=True, infinite=False)
    q, e = c_scene.getSoilEnergy()

    print("Incident energy: %f , horizontal irradiance: %f" % (e, q))
    
    print("--- done")