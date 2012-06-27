#
#
#       Python interface caribu and deals with its I/O
#

from caribu import Caribu
from label import Label
from CaribuScene import CaribuScene

from itertools import groupby, izip

def _caribu_call(canopy, lightsource, optics, pattern, options):
    """
    low level interface to Caribu class call
    Caribu allows nested radiosity illumination on a 3D scene.
    """
    
    sim = Caribu(resdir = None, resfile = None)#no output on disk
    # --canfile 
    sim.scene = canopy
    # --optics 
    sim.opticals = optics
    #--skyfile 
    sim.sky = lightsource               
    #--pattern 
    sim.pattern = pattern
    #--options (if different from caribu defaults)
    if options is not None:
        #--scatter
        if '1st' in options.keys():
            sim.direct= options['1st']
        #--nb_layers
        if 'Nz' in options.keys():
            sim.nb_layers =  options['Nz'] 
        #--can_height
        if 'Hc' in options.keys():
            sim.can_height =  options['Hc'] 
        #--sphere_diameter
        if 'Ds' in options.keys():
            sim.sphere_diameter =  options['Ds']
        #--debug mode (if True, prevent removal of tempdir)
        if 'debug' in options.keys():
            sim.my_dbg = options['debug']
        #--names of optical properties (usefull if opticals are given as strings
        if 'wavelength' in options.keys():
            sim.optnames = options['wavelength']
    status = str(sim)
    sim.run()
    irradiances=sim.nrj

    # return outputs
    return irradiances,status


def _nan_to_zero(x):

    try:
	from math import isnan
    except:
         #to be back compatile with python 2.5
	 def isnan(num):
	     return num != num
	 
    return(0 if isnan(x) else x)

def _output_dict(vcdict):
    '''    adaptor from nrj dict to  nrj + aggregation keys dict
    '''
    d = vcdict[vcdict.keys()[0]]['data']
    for k in ('Eabs','Ei_inf','Ei_sup'):
        d[k] = map(_nan_to_zero,d[k])
    eabs = [e * a for e,a in zip(d['Eabs'],d['area'])]
    labels = [Label(lab) for lab in d['label']]
    opt = [lab.optical_id for lab in labels]
    opak = [lab.transparency for lab in labels]
    plt = [lab.plant_id for lab in labels]
    elt = [lab.elt_id for lab in labels]

    godict = {'Eabs':eabs, 'Area':d['area'],'Eabsm2':d['Eabs'],'EiInf':d['Ei_inf'],'EiSup':d['Ei_sup'],'Opt':opt,'Opak':opak,'Plt':plt,'Elt':elt,'label':d['label']} 
  
    return godict


def caribu(caribuscene, direct = True, nz = None, dz = None, ds = None):
    '''functional interface to Caribu    
    '''
    scene = None
    lightsources = None
    pattern = None
    if caribuscene.hasScene:    
        scene = caribuscene.scene
    if caribuscene.hasSources:
        lightsources = caribuscene.sources
    opticals = caribuscene.PO
    if caribuscene.hasPattern:
        pattern = caribuscene.pattern
    optiondict = {'1st':direct,'Nz':nz,'Hc':dz,'Ds':ds,'wavelength':caribuscene.wavelength}
   
    vcout,status = _caribu_call(scene, lightsources, opticals, pattern, optiondict)
    
    return _output_dict(vcout)

def agregate(values,indices,fun = sum):
    """ performss aggregation of outputs along indices """
    ag = {}
    for key,group in groupby(sorted(izip(indices,values),key=lambda x: x[0]),lambda x : x[0]) :
        ag[key] = fun([elt[1] for elt in group])
    return ag
