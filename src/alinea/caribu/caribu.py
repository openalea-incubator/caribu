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


def radiosity(triangles, materials, lights, domain=None, mixed_radiosity=None,
              screen_size=1536):
    """Compute triangles illumination using radiosity model.

    Args:
        triangles:  (list of triangles) Each triangle is defined as
                   a triplet of oriented points in 3D space.
        materials: (list of optical materials)  # TODO
        lights: (list of lights)
        domain: (tuple of floats) Domain for repetition of the scene
                 (xmin, ymin, xmax, ymax) scene is not bounded along z axis
                 if None (default), scene is not repeated
        mixed_radiosity: (float, int, float) parameters used for mixed
                         radiosity computation (default None, pure radiosity)
                         or (radius, nb_layers, height):
                          - radius: distance for radiosity effects
                          - nb_layers: vertical subdivisions of scene
                          - height: maximum height of scene
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
    del mixed_radiosity
    del screen_size
