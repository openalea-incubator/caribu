#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os, sys
pj = os.path.join

from setuptools import setup, find_packages
from openalea.deploy.metainfo import read_metainfo

# Reads the metainfo file
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    if key != 'long_description':
        exec("%s = '%s'" % (key, value))

long_description = """ %s """ %(metadata['long_description'])
pkg_root_dir = 'src'

# dependencies 
setup_requires = ['openalea.deploy']
if ("win32" in sys.platform):
    install_requires = ['VPlants.PlantGL']
else:
    install_requires = []
dependency_links = ['http://openalea.gforge.inria.fr/pi']

# Scons build directory
build_prefix= "build-scons"

#retrieving packages
pkgs = [ pkg for pkg in find_packages(pkg_root_dir) if namespace not in pkg]
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('',pkg_root_dir)] + [(namespace + "." + pkg, pkg_root_dir + "/" + pkg) for pkg in top_pkgs] )
wralea_entry_points = ['%s = %s'%(pkg,namespace + '.' + pkg) for pkg in top_pkgs]

# Call to setup
setup(
    name=name,
    version=version,
    description=description,
    long_description="""%s"""%long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    packages= packages,    
    package_dir= package_dir,
    namespace_packages = [namespace],
    create_namespaces = True,
    zip_safe= False,
    setup_requires = setup_requires,
    install_requires = install_requires,
    dependency_links = dependency_links,                  
    # Include data
    include_package_data = True,
    package_data = {'' : ['*.can', '*.R', '*.8', '*.opt', '*.light', '*.csv', '*.png','*.pyd', '*.so', '*.dylib']},
    # Binary construction and install
    scons_scripts = ['SConstruct'],
    bin_dirs = {'bin':  build_prefix + '/bin'},
    # extensions
    entry_points = { 'wralea':  wralea_entry_points },
   )



    
