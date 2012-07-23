import os
import string
import numpy as np

from StringIO import StringIO
from itertools import groupby, izip
from openalea.plantgl.all import Tesselator

from caribu import Caribu
from label import Label

def _is_iterable(x):
    try:
        x = iter(x)
    except TypeError: 
        return False
    return True
    
    
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
        #filter negative values occuring in EiInf/EiSup
        d[k] = map(lambda(x): max(0,x), d[k])
    eabs = [e * a for e,a in zip(d['Eabs'],d['area'])]
    einc = [(esup + einf) * a for esup,einf,a in zip(d['Ei_sup'],d['Ei_inf'],d['area'])]
    labels = [Label(lab) for lab in d['label']]
    opt = [lab.optical_id for lab in labels]
    opak = [lab.transparency for lab in labels]
    plt = [lab.plant_id for lab in labels]
    elt = [lab.elt_id for lab in labels]

    godict = {'Eabs':eabs, 'Einc': einc,'Area':d['area'],'Eabsm2':d['Eabs'],'EiInf':d['Ei_inf'],'EiSup':d['Ei_sup'],'Opt':opt,'Opak':opak,'Plt':plt,'Elt':elt,'label':d['label']} 
  
    return godict
    
def _agregate(values,indices,fun = sum):
    """ performss aggregation of outputs along indices """
    ag = {}
    for key,group in groupby(sorted(izip(indices,values),key=lambda x: x[0]),lambda x : x[0]) :
        ag[key] = fun([elt[1] for elt in group])
    return ag
    
DefaultOptString = """#PyCaribu : PO par defaut (PAR, materiau vert)
#format e : tige,  feuille sup,  feuille inf
# nbre d'especes
n 1
#1 Sol
s d 0.15
# espece 1
e d 0.10   d 0.10 0.05  d 0.10 0.05
"""

#
# interfaces to generate caribu files line strings
#


#TO DO (June 2012): caribu scene should handle list of lines, and make the string at the time of writting, so that add_shape,addlight methods could be easily implemented

def _getlabel(line):
    ''' extract a label string from a can file line '''
    line = line.strip()
    if not line: 
        return
    if line[0] == '#':
        return 
    l = line.split()
    label = l[2]
    if len(label) < 11:
        label = (12-len(label))*'0'+label

    return label
    
def _lightString(lightVect):
    """ Create a line for caribu .light files from a vector specifying energy,posx, posy and posz of a light source"""
    return ' '.join(map(str,lightVect)) + '\n'

def _canString(ind, pts, label):
    s = "p 1 %s 3 %s"%(str(label), ' '.join('%.6f'%x for i in ind for x in pts[i]))
    return s + '\n'

def _shape_to_can(shape,tesselator,optid = 1,opak = 0,plant_id = 1,elt_id = 1):
    """
    Returns canestra string representation of a plantGL shape
    """

    shape.apply(tesselator)
    mesh = tesselator.triangulation
    pts = np.array(mesh.pointList, ndmin=2)
    indices = np.array(mesh.indexList, ndmin=2)
    _label = label.Label()
    _label.plant_id = plant_id
    _label.optical_id = optid
    _label.leaf_id = opak
    _label.elt_id = elt_id
    return [_canString(ind, pts, _label) for ind in indices]

class CaribuSceneError(Exception): pass

class CaribuScene(object):
    """  Handles CaribuScene """
    # Contient le texte des fichiers necessaires a canestra ou produit par lui (scene, 8, opt, ligtht, FF)
    #Contient les methode pou les brique caribu, l'extraction de donnees et la conversion vers plantGL pour visualisation

    
    def __init__(self, scene=None, light=None, pattern=None, opt=None, waveLength ='defaultPO'):
    
        self.hasScene = False
        self.scene = ""
        self.scene_labels = []#list of external identifier/canlabel of each triangle present in the scene
        self.scene_ids = []#list of internal ids, as long as scene, used to aggegate outputs by primitive
        self.cid = 1#internal id to be given to the next primitive     
        if scene is not None:
            if os.path.isfile(str(scene)):
                fin = open(scene)
                self.addCan(fin.read())
                fin.close()
            elif isinstance(scene, str):
                self.addCan(scene)
            else:
                try:
                    self.add_Shapes(scene)
                except:
                    raise CaribuSceneError("Scene should be one of : None, filename, file content (string)  or plantgl scene or shape")
                
        self.hasSources = False
        self.sources = "NoLightSources"
        if light is not None:
            if os.path.isfile(str(light)):
                fin = open(light)
                self.setSources(fin.read())
                fin.close()
            elif isinstance(light,str):
                self.setSources(light)
            else:
                try:
                    self.setSources_tuple(light)
                except:
                    pass
                    
        self.hasPattern = False
        self.pattern = "NoPattern"      
        if pattern is not None:
            if os.path.isfile(str(pattern)):
                fin = open(pattern)
                self.setPattern(fin.read())
                fin.close()
            elif isinstance(pattern,str):
                self.setPattern(pattern)
            else:
                try:
                    pat = '\n'.join([' '.join(map(str,pattern[0])),' '.join(map(str,pattern[1])),' '])
                    self.setPattern(pat)
                except:
                    pass

        self.PO = DefaultOptString
        self.wavelength = "defaultPO"
        if opt is not None:
            if os.path.isfile(str(opt)):
                waveLength=os.path.basename(opt).split('.')[0]
                fin = open(opt)
                self.setOptical(fin.read(),waveLength)
                fin.close()
            elif isinstance(opt,str):
                self.setOptical(opt,waveLength)
        
        self.hasFF = False
        self.FF = "NoFF"
        self.output = {}
    
    def resetScene(self):
        ''' Reset scene '''
        self.hasScene = False
        self.scene = ""
        self.scene_ids = []
        self.scene_labels = []
        self.cid = 1
     
    
    def addCan(self,canstring):
        '''  Add primitives from can file string '''
        self.scene += canstring
        self.hasScene = True
        labels = [res for res in (_getlabel(x) for x in canstring.splitlines()) if res]
        labmap = dict([(k,i) for i,k in enumerate(set(labels))])
        self.scene_labels.extend(labels)
        self.scene_ids.extend([self.cid + labmap[k] for k in labels])
        self.cid += len(labmap)
        return labmap
        
    def addSoil(self):
        ''' Add Soil to Caribu scene. Soil dimension is taken from pattern '''
        
        ids = []
        
        if not self.hasPattern:
            print('addSoil needs a pattern to be set')
            
        else:
            pat = self.pattern
            xy=map(string.split,pat.splitlines())
            A = map(float,xy[0])
            C = map(float,xy[1])
            if (A[0] > C[0]):
                A=map(float,xy[1])
                C=map(float,xy[0])
            if (C[1] < A[1]):
                D=[A[0],C[1]]        
                B=[C[0],A[1]]
            else:
                B=[A[0],C[1]]        
                D=[C[0],A[1]]
            A.append(0.)
            B.append(0.)
            C.append(0.)
            D.append(0.)

            label=["000000000000","000000000001"]
            canstring = "\n".join([_canString(range(3),(A,B,C),label[0]),_canString(range(3),(C,D,A),label[1])])
            ids = [self.cid,self.cid + 1]
 
            self.scene += canstring
            self.scene_ids.extend(ids)
            self.scene_labels.extend(label)
            self.hasScene = True
            self.cid += 2
        
        return dict(zip(label,ids))
        
    def add_Shapes(self, shapes, tesselator = None, opt_id = 1, opak = 0, plant_id = 1, elt_id = 1):
        """
        Add shapes to scene and return map of shapes id to carbu internal ids
        """
        if not tesselator:
            tesselator = Tesselator()
        
        if isinstance(opt_id,dict):
            optdict = opt_id
            defopt = 1
        else:
            optdict = {}
            defopt = opt_id

        if isinstance(opak,dict):
            opakdict = opak
            defopak = 0
        else:
            opakdict = {}
            defopak = opak

        if isinstance(plant_id,dict):
            pdict = plant_id
            defplant = 1
        else:
            pdict = {}
            defplant = plant_id

        if isinstance(elt_id,dict):
            edict = elt_id
            defelt = 1
        else:
            edict = {}
            defelt = elt_id

        canscene = []
        ids = []
        labels = []
        idmap={}
        
        if not _is_iterable(shapes):
            shapes = [shapes]
        
        for shape in shapes:
            canlines = _shape_to_can(shape,tesselator,optdict.get(shape.id,defopt),opakdict.get(shape.id,defopak),pdict.get(shape.id,defplant),edict.get(shape.id,defelt))
            canscene.extend(canlines)
            idmap[shape.id] = self.cid 
            ids.extend([self.cid] * len(canlines))
            labels.extend([shape.id] * len(canlines))
            self.cid += 1
        canstring = ''.join(canscene)
        
        self.scene += canstring
        self.scene_ids.extend(ids)
        self.scene_labels.extend(labels)
        self.hasScene = True
        
        return idmap


    def setCan_fromShapes(self,shapes,tesselator=None,opt_id = 1,opak = 0, plant_id = 1, elt_id = 1):
        """ Set canopy from PlantGl shapes and PGL tesselator and dict indexed by shapes_id of optical property indices, opacity, plantnumber and element number

        returns a list of shape ids as long as the primitives set in the canScene to allow aggregation of outputs
        """
        if isinstance(opt_id,dict):
            optdict = opt_id
            defopt = 1
        else:
            optdict = {}
            defopt = opt_id

        if isinstance(opak,dict):
            opakdict = opak
            defopak = 0
        else:
            opakdict = {}
            defopak = opak

        if isinstance(plant_id,dict):
            pdict = plant_id
            defplant = 1
        else:
            pdict = {}
            defplant = plant_id

        if isinstance(elt_id,dict):
            edict = elt_id
            defelt = 1
        else:
            edict = {}
            defelt = elt_id

        canscene = []
        ids = []
        canscene.append('# File generated by Alinea.Caribu.CaribuScene class\n')
        for shape in shapes:
            canlines = _shape_to_can(shape,tesselator,optdict.get(shape.id,defopt),opakdict.get(shape.id,defopak),pdict.get(shape.id,defplant),edict.get(shape.id,defelt))
            canscene.extend(canlines)
            ids.extend([shape.id] * len(canlines))
        canscene.append('\n')
        canstring = ''.join(canscene)
        self.addCan(canstring)
        return ids
    

    def setPattern(self,pattern_string):
        """  Set pattern """
        # re-order pattern to get xmin,ymin then xmax,ymax (needed for periodise to function correctly)
        p = pattern_string.splitlines()
        x1 = float(p[0].split()[0])
        y1 = float(p[0].split()[1])
        x2 = float(p[1].split()[0])
        y2 = float(p[1].split()[1])
        pattern_tuple = [(min(x1,x2),min(y1,y2)),(max(x1,x2),max(y1,y2))]
        pattern = '\n'.join([' '.join(map(str,pattern_tuple[0])),' '.join(map(str,pattern_tuple[1])),' '])
        self.pattern = pattern
        self.hasPattern = True

    def setOptical(self,optstring,wavelength):
        """  Set optical properties """
        self.PO = optstring
        self.wavelength = wavelength

    def setSources(self,sources_string):
        """  Set Light Sources """
        self.sources = sources_string
        self.hasSources = True

    def setSources_tuple(self,sources_tuples):
        """ Set light sources from a list of light tuples describing sources """
        lines = map(_lightString,sources_tuples)
        self.setSources(''.join(lines))

    def setFF(self,FF_string):
        """  Set Form factor matrix """
        self.FF = FF_string
        self.hasFF = True

    def setFF(self,FFfile):
        """  Set form factors from ff file """
        if os.path.isfile(FFfile):
            fin = open(FFfile)
            self.FF = fin.read()
            self.hasFF = True
            fin.close()


    def writeCan(self,canfile):
        """  write a canfile of the scene """ 
        if not self.hasScene:
            print "!!!Warning!!! CaribuScene has no Scene !"
        fout = open(canfile,"w")
        fout.write(self.scene)
        fout.close()

    def writePattern(self,patternfile):
        """  write a pattern file of  the scene """ 
        if not self.hasPattern:
            print "!!!Warning!!! CaribuScene has no Pattern !"
        
        fout = open(patternfile,"w")
        fout.write(self.pattern)
        fout.close()

    def writeOptical(self,optfile):
        """  write an optical file of  the scene """
        if self.wavelength == "defaultPO":
            print "!!!Warning!!! No PO specified, using default PO (see CaribuScene) !"
        fout = open(optfile,"w")
        fout.write(self.PO)
        fout.close()
    
    def sources_as_array(self):
        ''' returns a recarray of light sources charactecristics '''
        sources = None
        if self.hasSources:
            sources = np.recfromtxt(StringIO(self.sources), names = 'energy,vx,vy,vz')
        return sources
        
    def pattern_as_array(self):
        ''' Return a recarray of coordinates of the domain sepcified in pattern'''
        
        domain = None
        if self.hasPattern:
            domain = np.recfromtxt(StringIO(self.pattern), names = 'x,y')
        return domain
        
    def getIncidentEnergy(self):
        """ Computes Qi, Qem, Einc on the scene given current light sources

        Qi is the incident light flux received on an horizontal surface (per scene unit area)
        Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
        Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set

        """
        Qi, Qem, Einc = None,None,None

        if self.hasSources:
            sources = self.sources_as_array()
            
            Qi = sources.energy.sum()
            
            k = np.array([0,0,1])
            if sources.size <= 1:
                proj = abs(k.dot(np.array([sources.vx,sources.vy,sources.vz])))
            else:
                proj = [abs(k.dot(np.array([sources.vx[i],sources.vy[i],sources.vz[i]]))) for i in range(sources.size)]
            Qem = (sources.energy / proj).sum()
            
            if self.hasPattern:
                domain = self.pattern_as_array()
                d_area = abs(np.diff(domain.x) * np.diff(domain.y))[0]
                Einc = Qi * d_area

        return Qi,Qem,Einc

    def writeLight(self,lightfile):
        """  write a lightfile of the sources """ 
        if not self.hasSources:
            print "!!!Warning!!! CaribuScene has no ligth sources !"
        fout = open(lightfile,"w")
        fout.write(self.sources)
        fout.close()

    def writeFF(self,FFfile):
        """  write a FFfile of the scene """ 
        if not self.hasFF:
            print "!!!Warning!!! CaribuScene has no FormFactor yet !"
        fout = open(FFfile,"w")
        fout.write(self.FF)
        fout.close()
    
    def __str__(self):
        s = """
Pattern: 
%s

Current Wavelength : %s
PO:
%s

has FF: %s
Light Sources:
%s
Scene:
%s
"""%(self.pattern,
    self.wavelength,
    self.PO,
     str(self.hasFF),
    '\n'.join(self.sources.splitlines()[0:5])+'...',
     '\n'.join(self.scene.splitlines()[0:7])+'...')
        return s
    
    def run(self, direct = True, nz = None, dz = None, ds = None):
        ''' Call Caribu and store relsults'''
        scene = None
        lightsources = None
        pattern = None
        if self.hasScene:    
            scene = self.scene
        if self.hasSources:
            lightsources = self.sources
        opticals = self.PO
        if self.hasPattern:
            pattern = self.pattern
        optiondict = {'1st':direct,'Nz':nz,'Hc':dz,'Ds':ds,'wavelength':self.wavelength}
   
        vcout,status = _caribu_call(scene, lightsources, opticals, pattern, optiondict)
    
        self.output = _output_dict(vcout)
        
    def getOutput(self,var = 'Eabs',aggregate = True):
        ''' Returns outputs'''
        
        if aggregate:
            res = _agregate(self.output[var],self.scene_ids)
        else: 
            res = _agregate(self.output[var],self.scene_ids,list)
        return(res)

        
def newCaribuScene(scene,light,pattern,opt):
    cs = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    return cs
    
    
def addShapes(caribuscene,shapes,tesselator, opt_id = 1, opak = 0, plant_id = 1, elt_id = 1):
    mid=caribuscene.add_Shapes(shapes,tesselator,opt_id, opak, plant_id, elt_id)
    return caribuscene,mid 
    
def getOutput(caribuscene,var,aggregate):
    return caribuscene.getOutput(var,aggregate)


def runCaribu(caribuscene, direct = True, nz =10,dz=1,ds=0.5):
    '''functional interface to Caribu    
    '''
    caribuscene.run(direct,nz,dz,ds)
    return caribuscene


def newFileCaribuScene(canfile,lightfile,patternfile=None,optfile=None):
    return CaribuScene(canfile,lightfile,patternfile,optfile)


def newObjCaribuScene(scene_obj=None,ligth_string=None,pattern_tuple=None,opt_string=None,waveLength=None):
    return CaribuScene(scene_obj,ligth_string,pattern_tuple,opt_string,waveLength)

def getIncidentEnergy(caribu_scene):
    return caribu_scene.getIncidentEnergy()

