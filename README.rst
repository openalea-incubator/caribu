=============
alinea.caribu
=============

.. {# pkglts, doc

.. image:: https://travis-ci.org/openalea-incubator/caribu.svg?branch=master
    :alt: Travis build status
    :target: https://travis-ci.org/openalea-incubator/caribu

.. #}

What is Caribu ?
----------------

Caribu is a modelling suite for lighting 3D virtual scenes, especially designed
for the illumination of virtual plant canopies such as virtual crop fields.
It uses a special algorithm, the nested radiosity (Chelle et al., 1998), that
allows for a precise estimation of light absorption at the level of small
canopy elements (typically 1 cm2). It takes into account multiple scattering,
allows for infinitisation of the scene (by virtual replication) and performs
in a reasonable time (typically a few minutes).

The idea is to mix a projection model that solves the first order illumination,
a model that solves the radiosity equations for the ligth exchanges between a
canopy element and its close neighbourhood, and a model that solves turbid
medium equations for the exchanges between a canopy element and the rest of
the canopy.


Content
'''''''

The suite is composed of two main sub-models : MCSail, that computes turbid
medium equations on a layered canopy and Canestra, that computes radiosity
and projection. The suite also includes two utililities : periodise, that
makes a scene suitable for infinite replication and S2v, that transforms a
3D scene in a 1D multi-layer system.

It operates on a special scene object called Caribuscene, composed of a list
of triangles with optical properties representing the plants, a set of
direction and intensities (called light sources) representing the sky and
a pattern delimiting the scene, used for infinitisation.

This model is completed with a set of utilities for visualisation
(using PlantGL), import of caribuscene from files or MTG, and tools for
building ligth sources from meteorological data


Installation
------------

.. toctree::
    :maxdepth: 2

    ./install/install.rst

Documentation
-------------

Notebook
''''''''

.. toctree::
    :maxdepth: 2

    ./notebook/notebook.rst


References
''''''''''

.. toctree::
    :maxdepth: 4

    ./_dvlpt/modules.rst

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Authors
-------

.. include:: ../AUTHORS.rst

Contributing
------------

.. toctree::

    ./contributing.rst

License
-------

**Caribu** is released under a specific INRA License agreement. See LICENSE
file.

