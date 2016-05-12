"""base Pythonic functions to call caribu shell.
"""


def raycasting(triangles, materials, lights, domain=None, screen_size=1536):
    """Compute triangles illumination using raycasting model.

    Args:
        triangles: (list of triangles) Each triangle is defined as
                   a triplet of oriented points in 3D space.
        materials: (list of optical materials)  # TODO
        lights: (list of lights)
        domain: (tuple of floats) Domain for repetition of the scene
                 (xmin, ymin, xmax, ymax) scene is not bounded along z axis
                 if None (default), scene is not repeated
        screen_size: (int) buffer size for projection images

    Returns:
        (dict of str:property) properties computed:
          - Ei
          - Ei_min
          - Ei_max
    """
    del triangles
    del materials
    del lights
    del domain
    del screen_size


def radiosity():
    pass
