# -*- python -*-
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       WebSite : https://github.com/openalea-incubator/caribu
#
# ==============================================================================
from math import *


def lightString(radiance, zenith_angle, azimuth_angle):
    '''    compute the directional vector from zenith and azimuth angles
    '''
    theta = zenith_angle / 180. * pi
    phi = azimuth_angle / 180. * pi
    vector = (radiance, sin(theta) * cos(phi),sin(theta) * sin(phi),  - cos(theta)) 
    return  ' '.join(map(str,vector))
