import os
import string
import label
from numpy import array
from itertools import groupby, izip
from caribu import Caribu
from label import Label

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


def _lightString(lightVect):
    """ Create a line for caribu .light files from a vector specifying energy,posx, posy and posz of a light source"""
    return ' '.join(map(str,lightVect)) + '\n'

def _canString(ind, pts, label):
    s = "p 1 %s 3 %s"%(str(label), ' '.join('%.6f'%x for i in ind for x in pts[i]))
    return s + '\n'

def shape_to_can(shape,tesselator,optid = 1,opak = 0,plant_id = 1,elt_id = 1):
    """
    Returns canestra string representation of a plantGL shape
    """

    shape.apply(tesselator)
    mesh = tesselator.triangulation
    pts = array(mesh.pointList, ndmin=2)
    indices = array(mesh.indexList, ndmin=2)
    _label = label.Label()
    _label.plant_id = plant_id
    _label.optical_id = optid
    _label.leaf_id = opak
    _label.elt_id = elt_id
    return [_canString(ind, pts, _label) for ind in indices]


class CaribuScene(object):
    """  Handles CaribuScene """
    # Contient le texte des fichiers necessaires a canestra ou produit par lui (scene, 8, opt, ligtht, FF)
    #Contient les methode pou les brique caribu, l'extraction de donnees et la conversion vers plantGL pour visualisation

    
    def __init__(self):
        self.hasScene = False
        self.scene = ""
        self.scene_ids = []#list of ids, as long as scene, used to aggegate outputs
        self.cid = 1#id to be given to next primitive
        self.hasPattern = False
        self.pattern = "NoPattern"
        self.PO = DefaultOptString
        self.wavelength = "defaultPO"
        self.hasSources = False
        self.sources = "NoLightSources"
        self.hasFF = False
        self.FF = "NoFF"
        self.output = {}

    def setCan(self,canstring):
        """  Set canopy from can file string """
        self.scene = canstring
        self.hasScene = True

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

            label="000000000000"
            canstring = "\n".join([_canString(range(3),(A,B,C),label),_canString(range(3),(C,D,A),label)])
            ids = [self.cid,self.cid + 1]
            self.scene += canstring
            self.scene_ids.extend(ids)
            self.cid += 2
        
        return ids
        
    def add_Shapes(self, shapes, tesselator, opt_id = 1, opak = 0, plant_id = 1, elt_id = 1):
        """
        Add shapes to scene and return map of shapes id to carbu internal ids
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
        idmap={}

        for shape in shapes:
            canlines = shape_to_can(shape,tesselator,optdict.get(shape.id,defopt),opakdict.get(shape.id,defopak),pdict.get(shape.id,defplant),edict.get(shape.id,defelt))
            canscene.extend(canlines)
            idmap[shape.id] = self.cid 
            ids.extend([self.cid] * len(canlines))
            self.cid += 1
        canstring = ''.join(canscene)
        if not self.hasScene:
            self.setCan(canstring)
        else: 
            self.scene += canstring
        self.scene_ids.extend(ids)
        return idmap


    def setCan_fromShapes(self,shapes,tesselator,opt_id = 1,opak = 0, plant_id = 1, elt_id = 1):
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
            canlines = shape_to_can(shape,tesselator,optdict.get(shape.id,defopt),opakdict.get(shape.id,defopak),pdict.get(shape.id,defplant),edict.get(shape.id,defelt))
            canscene.extend(canlines)
            ids.extend([shape.id] * len(canlines))
        canscene.append('\n')
        canstring = ''.join(canscene)
        self.setCan(canstring)
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

    def getIncidentEnergy(self):
        """ return the total ammount of energy emitted by the lights of the scene """
        Ei=0
        if self.hasSources:
            sources=self.sources.splitlines()
            for s in sources :
                l=s.strip()
                if not l or l.startswith('#'):
                    continue
                col=l.split()
                #filter empty lines
                if(not col) : continue
                Ei += float(col[0])

        return(Ei)

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
    cs = CaribuScene()
    if scene is not None:
        if os.path.isfile(scene):
            fin = open(scene)
            cs.setCan(fin.read())
            fin.close()
        elif isinstance(scene, str):
            cs.setCan(scene)
        
    if light is not None:
        if os.path.isfile(light):
            fin = open(light)
            cs.setSources(fin.read())
            fin.close()
        elif isinstance(light,str):
            cs.setSources(light)
        else:
            try:
                cs.setSources_tuple(light)
            except:
                pass
       
    if pattern is not None:
        if os.path.isfile(pattern):
            fin = open(pattern)
            cs.setPattern(fin.read())
            fin.close()
        elif isinstance(pattern,str):
            cs.setPattern(pattern)
        else:
            try:
                pat = '\n'.join([' '.join(map(str,pattern[0])),' '.join(map(str,pattern[1])),' '])
                cs.setPattern(pat)
            except:
                pass

    if opt is not None:
        if os.path.isfile(opt):
            waveLength=os.path.basename(opt).split('.')[0]
            fin = open(opt)
            cs.setOptical(fin.read(),waveLength)
            fin.close()
            
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

class FileCaribuScene(CaribuScene):
    """Adaptor to contruct CaribuScenes from files"""

    def __init__(self, canfile,lightfile,patternfile=None,optfile=None):
        CaribuScene.__init__(self)

        if os.path.isfile(canfile):
            fin = open(canfile)
            self.setCan(fin.read())
            fin.close()

        if os.path.isfile(lightfile):
            fin = open(lightfile)
            self.setSources(fin.read())
            fin.close()
       
        if (patternfile is not None) and os.path.isfile(patternfile):
            fin = open(patternfile)
            self.setPattern(fin.read())
            fin.close()

        if (optfile is not None) and os.path.isfile(optfile):
            waveLength=os.path.basename(optfile).split('.')[0]
            fin = open(optfile)
            self.setOptical(fin.read(),waveLength)
            fin.close()

def newFileCaribuScene(canfile,lightfile,patternfile=None,optfile=None):
    return FileCaribuScene(canfile,lightfile,patternfile,optfile)


class ObjCaribuScene(CaribuScene):
    """Adaptor to construct caribuScene from objects"""

    def __init__(self, scene_obj,light_string,pattern_tuple=None,opt_string=None,waveLength=None):
        CaribuScene.__init__(self)
        if scene_obj is not None:
            try:
                self.scene = scene_obj
            except AttributeError:
                print("Scene object input to ObjCaribuScene should have a to_canestra method")
                raise
            else:
                self.hasScene = True
        if light_string is not None:
            self.setSources(light_string)
        if pattern_tuple is not None:
            pat = '\n'.join([' '.join(map(str,pattern_tuple[0])),' '.join(map(str,pattern_tuple[1])),' '])
            self.setPattern(pat)
        if opt_string is not None and waveLength is not None:
            self.setOptical(opt_string,waveLength)

def newObjCaribuScene(scene_obj=None,ligth_string=None,pattern_tuple=None,opt_string=None,waveLength=None):
    return ObjCaribuScene(scene_obj,ligth_string,pattern_tuple,opt_string,waveLength)

def getIncidentEnergy(caribu_scene):
    return caribu_scene.getIncidentEnergy(),

