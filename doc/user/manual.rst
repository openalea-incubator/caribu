User guide
##########

.. toctree::

    QuickStart.rst

Visualea tutorial
---------------
This dataflow illustrate how to run the Caribu model using historical input files.
The different inputs are:
 - a scene geometry (collection of shapes)
 - a set of light sources
 - a file describing the scene boundary to use to make it toric
 - a file allowing to specify the optical property of the objects in the scene
 
CaribuScene is container for all these inputs, and is also compatible with other openalea objects (see Use :class:`CaribuScene <alinea.caribu.CaribuScene.CaribuScene>`)

The scene can be viewed with 'Plot CaribuScene', and the model run with the 'Caribu' node.

The following outputs are provided:

- a 3D colored scene, showing how light is distributed ('ViewMapOnCan')
- The light interception efficiency (ie total intercepted / total illuminating): 'LIE'
- an output file giving intercepted light for all objects in the scene ('Write Table')


.. dataflow:: alinea.caribu Tutorial


 