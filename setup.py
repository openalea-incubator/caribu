#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from os import walk
from os.path import abspath, normpath
from os.path import join as pj

from setuptools import setup, find_packages


short_descr = "Python/Visualea interface to Caribu Light model"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

# find version number in src/alinea/caribu/version.py
version = {}
with open("src/alinea/caribu/version.py") as fp:
    exec(fp.read(), version)


data_files = []

nb = len(normpath(abspath("src/caribu_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/caribu_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


setup_kwds = dict(
    name='alinea.caribu',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="openalea-incubator, Christian Fournier, ",
    author_email="openalea@inra.fr, Christian.Fournier@supagro.inra.fr, ",
    url='https://github.com/openalea-incubator/caribu',
    license='INRA_License_agreement',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    
    include_package_data=True,
    package_data={'caribu_data': data_files},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

build_prefix = "build-scons"
setup_kwds['scons_scripts'] = ['SConstruct']
setup_kwds['bin_dirs'] = {'bin': build_prefix + '/bin'}

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
