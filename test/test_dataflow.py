"""Caribu dataflow Tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.core import alea
from openalea.core.alea import run, function
from openalea.core.pkgmanager import PackageManager
from random import random, randint

""" A unique PackageManager is created for all test of dataflow """
#pm = PackageManager()
#pm.init(verbose=False)


def test_caribu():
    """ Test Tutorial LIE """

    res = run(('alinea.caribu', 'Tutorial'),
        inputs={}, vtx_id=11)
    #assert 0.62 < res[0] < 0.63, res

