#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

import os
from os import walk
from os.path import abspath, normpath, dirname
from os.path import join as pj

from setuptools import setup, find_namespace_packages

short_descr = "Python/Visualea interface to Caribu Light model"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/alinea/caribu/version.py
version = {}
with open("src/alinea/caribu/version.py") as fp:
    exec(fp.read(), version)
version_caribu = version["__version__"]

data_files = []

nb = len(normpath(abspath("src/caribu_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]

"""
for root, dnames, fnames in walk("src/caribu_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))
"""

setup_kwds = dict(
    name='alinea.caribu',
    version=version_caribu,
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Christian Fournier, Michael Chelle, Christophe Pradal ",
    author_email="Christian.Fournier@inrae.fr, m dot chelle at brgm dot fr, christophe dot pradal _at_ cirad fr ",
    url='https://github.com/openalea-incubator/caribu',
    license='CECILL-C',
    zip_safe=False,

    packages=find_namespace_packages(where='src', include=['alinea.*']),
    package_dir={'': 'src'},

    include_package_data=True,
    package_data={},
    entry_points={},
    keywords='openalea, FSPM, light',
    #test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

#setup_kwds['setup_requires'] = ['openalea.deploy']

build_prefix = pj(abspath(dirname(__file__)),"build-scons")
setup_kwds['scons_scripts'] = ['SConstruct']
setup_kwds['bin_dirs'] = {'bin': build_prefix + '/bin'}
setup_kwds['lib_dirs'] = {'lib' : build_prefix+'/lib' }
setup_kwds['inc_dirs'] = { 'include' : build_prefix+'/include' }
setup_kwds['entry_points']['wralea'] = ['alinea.caribu = alinea.caribu_wralea']
setup_kwds['package_data'][''] = ['*.can', '*.R', '*.8', '*.opt', '*.light', '*.csv', '*.png']

setup_kwds['setup_requires'] = ['openalea.deploy']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
