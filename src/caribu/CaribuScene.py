""" This module defines CaribuScene and CaribuSceneError classes."""

def _agregate(values,indices,fun = sum):
    """ performs aggregation of outputs along indices """
    from itertools import groupby, izip
    ag = {}
    for key,group in groupby(sorted(izip(indices,values),key=lambda x: x[0]),lambda x : x[0]) :
        vals = [elt[1] for elt in group]
        try:
            ag[key] = fun(vals)
        except TypeError:
            ag[key] = vals[0]
    return ag


def _get_triangle(line):
    from openalea.plantgl.all import Vector3
    line = line.strip()
    if not line: 
        return
    if line[0] == '#':
        return 
    l = line.split()
    nb_polygon = int(l[-10])
    assert nb_polygon == 3
    coords = map(float,l[-9:])   
    triangle = (Vector3(*coords[:3]), 
        Vector3(*coords[3:6]), 
        Vector3(*coords[6:]))
    return triangle


class CaribuSceneError(Exception): pass

class CaribuScene(object):
    """  Handles CaribuScene """
    # Contient le texte des fichiers necessaires a canestra ou produit par lui (scene, 8, opt, ligtht)
    #Contient les methode pou les brique caribu, l'extraction de donnees et la conversion vers plantGL pour visualisation

    
    def __init__(self, scene=None, light=None, pattern=None, opt=None, waveLength ='defaultPO'):
        """Initialise a Caribu Scene object.
        
        :Optional parameters:
        
        - `scene` is a filename (*.can), a string (can file format), a (list of) PlantGl shape(s) with ids or an object with a 'to_canestra' method (generating a string in can format)
        
        - `ligth` is a filename (*.light), a string (light file format) or a (list of) tuple (Energy, (vx, vy, vz))
        
        - `pattern` is a filename (*.8), a string (8 file format) or a tuple ((xmin,ymin), (xmax,ymax))
        
        - `opt` is a filename (*.opt) or a string (opt file format)
        
        File format specifications are in data/CanestraDoc.pdf


        """
        
        import os
        DefaultOptString = """#PyCaribu : PO par defaut (PAR, materiau vert)
#format e : tige,  feuille sup,  feuille inf
# nbre d'especes
n 1
#1 Sol
s d 0.15
# espece 1
e d 0.10   d 0.10 0.05  d 0.10 0.05
"""

 
        self.hasScene = False
        self.scene = ""
        self.scene_labels = []#list of external identifier/canlabel of each triangle present in the scene
        self.scene_ids = []#list of internal ids, as long as scene, used to aggegate outputs by primitive
        self.colors = {}#dict of id->(r,g,b) tuples of ambient colors of primitives
        self.pid = 1#internal pending id to be given to the next primitive

        if scene is not None:
            if hasattr(scene,'to_canestra'):
                canstring = scene.to_canestra()
                self.addCan(canstring)
            elif os.path.isfile(str(scene)):
                fin = open(scene)
                canstring = fin.read()
                fin.close()
                self.addCan(canstring)                
            elif isinstance(scene, str):
                self.addCan(scene)
            else:
                try:
                    self.add_Shapes(scene)
                except:
                    raise CaribuSceneError("Scene should be one of : None, filename, file content (string)  or plantgl scene or shape")
                
        self.hasSources = False
        self.sources = ""
        if light is not None:
            self.addSources(light)
                     
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
        
    
    def resetScene(self):
        """ Reset scene and output (keep opt, pattern and sources)"""
        self.hasScene = False
        self.scene = ""
        self.scene_ids = []
        self.scene_labels = []
        self.pid = 1
    
    def addCan(self,canstring, palette = {'leaf' : (0,180, 0), 'stem' : (0,130,0), 'soil' : (170, 85, 0)}):
        """  Add primitives from can file string """
        
        from alinea.caribu.label import Label
        
        def _getlabel(line):
            line = line.strip()
            if not line: 
                return
            if line[0] == '#':
                return 
            l = line.split()
            label = l[2]
            if len(label) < 11:
                label = (12 - len(label)) * '0' + label
            return label

        self.scene += canstring
        self.hasScene = True
        labels = [res for res in (_getlabel(x) for x in canstring.splitlines()) if res]
        labmap = dict([(k,i + self.pid) for i,k in enumerate(set(labels))])
        colormap = dict([(id,palette[Label(label).get_identity()]) for label,id in labmap.iteritems()])
        self.scene_labels.extend(labels)
        self.scene_ids.extend([labmap[k] for k in labels])
        self.colors.update(colormap)
        self.pid += len(labmap)
        return labmap
        
    def addSoil(self, zsoil = 0., color = (170, 85, 0)):
        """ Add Soil to Caribu scene. Soil dimension is taken from pattern.
        zsoil specifies the heigth of the soil

        """
        import string
        def _canString(ind, pts, label):
            s = "p 1 %s 3 %s"%(str(label), ' '.join('%.6f'%x for i in ind for x in pts[i]))
            return s + '\n'

        
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
            A.append(zsoil)
            B.append(zsoil)
            C.append(zsoil)
            D.append(zsoil)

            label=["000000000000","000000000001"]
            canstring = "\n".join([_canString(range(3),(A,B,C),label[0]),_canString(range(3),(C,D,A),label[1])])
            ids = [self.pid,self.pid + 1]
 
            self.scene += canstring
            self.scene_ids.extend(ids)
            self.scene_labels.extend(label)
            self.colors[self.pid] = color
            self.colors[self.pid + 1] = color
            self.hasScene = True
            self.pid += 2
        
        return dict(zip(label,ids))
        
    def add_Shapes(self, shapes, tesselator = None, canlabels = None):
        """Add shapes to scene and return a map of shapes id to caribu internal ids.
        """
        
        def _canString(ind, pts, label):
            s = "p 1 %s 3 %s"%(str(label), ' '.join('%.6f'%x for i in ind for x in pts[i]))
            return s + '\n'

        
        def _canString_fromShape(shape,tesselator,label = '100001000001'):
            import numpy
            shape.apply(tesselator)
            mesh = tesselator.triangulation
            pts = numpy.array(mesh.pointList, ndmin=2)
            indices = numpy.array(mesh.indexList, ndmin=2)
            return [_canString(ind, pts, label) for ind in indices]

        def _is_iterable(x):
            try:
                x = iter(x)
            except TypeError: 
                return False
            return True
             
            
        if not tesselator:
            from openalea.plantgl.all import Tesselator
            tesselator = Tesselator()
        
        if not _is_iterable(shapes):
            shapes = [shapes]
        
        if not canlabels:
            from alinea.caribu.label import encode_label
            canlabels = encode_label(minlength=len(shapes))
            
        canscene = []
        ids = []
        labels = []
        idmap={}
        
        for i,shape in enumerate(shapes):
            canlines = _canString_fromShape(shape,tesselator,canlabels[i])
            canscene.extend(canlines)
            idmap[shape.id] = self.pid 
            ids.extend([self.pid] * len(canlines))
            labels.extend([shape.id] * len(canlines))
            col = shape.appearance.ambient
            self.colors[self.pid] = (col.red,col.green,col.blue)
            self.pid += 1
        canstring = ''.join(canscene)
        
        self.scene += canstring
        self.scene_ids.extend(ids)
        self.scene_labels.extend(labels)
        self.hasScene = True
        
        return idmap
    

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

    def addSources(self,sources):
        """ Set light sources from a filename (*.light), a string (light file format) or(a list of) tuples (energy,(vx,vy,vz).
        energy is the light flux (per scene unit area) measured on an horizontal surface
        vx,vy,vz are the coordinates of the normalised vector of light direction 
        example : (1, (0, 0, -1)) is a source pointing downwards of intensity 1

        """
        import os
        if sources is not None:
            if os.path.isfile(str(sources)):
                fin = open(sources)
                sourcestring = fin.read()
                fin.close()
                self.addSources_from_string(sourcestring)                
            elif isinstance(sources,str):
                self.addSources_from_string(sources)
            else:
                try:
                    self.addSources_from_tuple(sources)
                except:
                    raise CaribuSceneError("Light sources should be one of : filename, file content (string)  or (list of ) tuple (Energy, (vx,vy,vz))")
       
    def addSources_from_string(self,sources):
        """  add Light Sources  from string or file name"""
        self.sources += sources
        self.hasSources = True

    def addSources_from_tuple(self,sources):
        """  add Light Sources  from a (energy, (vx,vy,vz)) (list of) tuple. """
        
        def _lightString(lightVect):
            e,p = lightVect
            return ' '.join(map(str,[e] + list(p))) + '\n'

        if not isinstance(sources,list):
            sources = [sources]    
        lines = map(_lightString,sources)
        self.addSources_from_string(''.join(lines))


    def generate_scene(self, colors = None):
        """
        Generate PlantGL scene from Caribu scene
        
        Colors is an (optional) list of (rgb) tuples specifiying colors of individual triangles in the scene

        """
        from openalea.plantgl.all import Scene, TriangleSet, Index3, Color4, Shape,Color3,Material
        
        scene = Scene()
        
        if len(self.scene_ids) > 0: #scene is not empty
            
            triangles = self.getTriangles()

            geoms = {}
            
            for i,triangle in enumerate(triangles):
                id = self.scene_ids[i]                
                if id not in geoms:
                    geoms[id] = TriangleSet([],[])
                    if colors:
                        geoms[id].colorList = []
                        geoms[id].colorPerVertex = False
                shape = geoms[id]
                count = len(shape.pointList)
                shape.pointList.append(triangle[0])
                shape.pointList.append(triangle[1])
                shape.pointList.append(triangle[2])
                shape.indexList.append(Index3(count, count+1,count+2))
                if colors:
                    r,g,b = colors[i]
                    shape.colorList.append(Color4(r,g,b,0))
                    
            for id,geom in geoms.iteritems():
                if colors:
                    shape = geom
                    shape.id = id
                else:
                    material = Material(Color3(*self.colors[id]))
                    shape = Shape(geom, material)
                    shape.id = id
      
                scene += shape
            
            
        return(scene)
        
    def writeCan(self,canfile):
        """  write the scene in a file (can format) """ 
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
        """ returns a recarray of light sources charactecristics """
        from numpy import recfromtxt
        from StringIO import StringIO
        sources = None
        if self.hasSources:
            sources = recfromtxt(StringIO(self.sources), names = 'energy,vx,vy,vz')
        return sources
        
    def pattern_as_array(self):
        """ Return a recarray of coordinates of the domain sepcified in pattern"""
        from numpy import recfromtxt
        from StringIO import StringIO
        domain = None
        if self.hasPattern:
            domain = recfromtxt(StringIO(self.pattern), names = 'x,y')
        return domain
        
    def getIncidentEnergy(self):
        """ Compute Qi, Qem, Einc on the scene given current light sources.

        Qi is the incident light flux received on an horizontal surface (per scene unit area)
        Qem is the sum of light fluxes emitted by sources in a plane perpendicular to their direction of emmission (per scene unit area)
        Einc is the total incident energy received on the domain (Einc = Qi * domain_area), or None if pattern is not set

        """
        import numpy
        Qi, Qem, Einc = None,None,None

        if self.hasSources:
            sources = self.sources_as_array()
            
            Qi = sources.energy.sum()
            
            # costheta = k . direction, k etant le vecteur (0,0,1) et theta l'angle avec la verticale = abs(zdirection) / norm(direction)
            norm = numpy.sqrt(sources.vx**2 + sources.vy**2 + sources.vz**2)
            costheta = abs(sources.vz) / norm
            Qem = (sources.energy / costheta).sum()
            
            if self.hasPattern:
                domain = self.pattern_as_array()
                d_area = abs(numpy.diff(domain.x) * numpy.diff(domain.y))[0]
                Einc = Qi * d_area

        return Qi,Qem,Einc

    def getOptical(self):
        """ return a list of tuple (reflectance, transmitance) for all triangles in the scene
        """
        from label import Label
        def _reftrans(label, po):
            if label.is_soil():
                res = (po['albedo'], 0, 0, 0)
            else:
                esp = label.optical_id
                opts = po['species'][esp]
                if label.is_stem():
                    res = (opts[0], 0, 0, 0)
                else:
                    res = (opts[1:])
            return res
            
        labels = map(Label,self.scene_labels)
        # pase opt (in getPO)
        #self.PO.splitlines()
        po = {'albedo' : 0.2, 'species' : {1:(10,1,1,1,1),2:(20,2,2,2,2)}}
        return [_reftrans(lab,po) for lab in labels]
    
    def getTriangles(self):
        """ return a list of  triangles in the scene
        """
        canstring = self.scene
        return [res for res in (_get_triangle(x) for x in canstring.splitlines()) if res]

    
    def getNormals(self):
        """ return a list of normals (as pgl.vector3) for all triangles in the scene
        """
        from openalea.plantgl.all import cross
        def _normal(triangle):
            A,B,C = triangle
            n = cross(B-A, C-A)
            return n.normed()
            
        triangles = self.getTriangles()
        return [_normal(tri) for tri in triangles]

    def getCenters(self):
        """ return a list of center coordinates for all triangles in the scene
        """
        def _center(triangle):
            A,B,C = triangle
            return (A + B + C) / 3.
           
        triangles = self.getTriangles()
        return [_center(tri) for tri in triangles]

    
    def writeLight(self,lightfile):
        """  write a lightfile of the sources """ 
        if not self.hasSources:
            print "!!!Warning!!! CaribuScene has no ligth sources !"
        fout = open(lightfile,"w")
        fout.write(self.sources)
        fout.close()

    
    def __str__(self):
        s = """
Pattern: 
%s

Current Wavelength : %s
PO:
%s


Light Sources:
%s
Scene:
%s
"""%(self.pattern,
    self.wavelength,
    self.PO,
    '\n'.join(self.sources.splitlines()[0:5])+'...',
     '\n'.join(self.scene.splitlines()[0:7])+'...')
        return s
    
    
    def get_caribu_output(self,vcdict):
        """ Get, filter and arrange output of caribu for use in CaribuScene. """
                           
        from itertools import izip
        
        def _nan_to_zero(x):
            try:
                from math import isnan
            except:
                 #to be back compatile with python 2.5
                def isnan(num):
                    return num != num         
            return(0 if isnan(x) else x)
            
        d = vcdict[vcdict.keys()[0]]['data']
        # compute max value = sum of emmission of sources
        _,eimax,_ = self.getIncidentEnergy()
        for k in ('Ei_inf','Ei_sup','Eabs'):
            d[k] = map(_nan_to_zero,d[k])
            #filter negative values occuring in EiInf/EiSup and values > Eimax
            d[k] = map(lambda(x): min(eimax,max(0,x)), d[k])
        eabs = [e * a for e,a in izip(d['Eabs'],d['area'])]
        einc = [(esup + einf) * a for esup,einf,a in izip(d['Ei_sup'],d['Ei_inf'],d['area'])]
        ei = [esup + einf for esup,einf in izip(d['Ei_sup'],d['Ei_inf'])]
        eincsup = [esup * a for esup,a in izip(d['Ei_sup'],d['area'])]
        eincinf = [einf * a for einf,a in izip(d['Ei_inf'],d['area'])]
     
        csdict = {'Eabs': eabs, 'Einc': einc, 'Ei': ei, 'EincSup': eincsup, 'EincInf': eincinf, 
                  'Area': d['area'],
                  'Eabsm2': d['Eabs'], 'EiInf': d['Ei_inf'], 'EiSup': d['Ei_sup'],
                  'label': d['label']} 
        return csdict  
    
    def runCaribu(self, direct = True, nz = 10, dz = 5, ds = 0.5, infinity = True):
        """ Call Caribu and return results"""
        
        output = {}
        if len(self.scene_ids) > 0: #scene is not empty
            from alinea.caribu.caribu import vcaribu            
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
            optiondict = {'1st':direct,'Nz':nz,'Hc':dz,'Ds':ds,'infinity': infinity, 'wavelength':self.wavelength}
       
            vcout,status = vcaribu(scene, lightsources, opticals, pattern, optiondict)
            output = self.get_caribu_output(vcout)

        return(output)


    def runPeriodise(self):
        """ Call periodise and modify position of triangle in the scene to fit inside pattern"""
        if len(self.scene_ids) > 0: #scene is not empty
            from alinea.caribu.caribu import vperiodise            
            scene = None
            pattern = None
            if self.hasScene:    
                scene = self.scene
            if self.hasPattern:
                pattern = self.pattern
            newscene = vperiodise(scene, pattern)
            self.scene = newscene
            
    
    def output_by_id(self, output, mapid = None, groups = None, aggregate = True):
        """ Return caribu outputs grouped or aggregated by ids 
        mapid: a dict of external_id -> caribu internal id. If given, the results are given for external _ids
        groups : a dict of id (internal of external) -> group_id. If given, results are computed for each group_id. Keys in groups are expected to be internal id if mapid is none, or external ids if mapid is given.
        if aggregate is True, one scalar is return by id (sum or weighted mean), otherwise it returns the list of values of all triangles of the id.

        
        """
        #
        #+ une fonction input_by_id qui renverrai hmin, hmax, h, normale, azimuth, area et lai pour differents aggregateurs
        res = {}        
        if len(output) > 0:           
            indices = self.scene_ids
            
            if groups:
                new_map = {} #dict of group_id -> reference internal id (reference id is the first one found belonging to a group)
                aliases = {} #dict of internal_id -> reference id of a group
                for id in groups:
                    gid = groups[id]
                    if mapid:
                        id = mapid[id]
                    if gid in new_map:
                        aliases[id] = new_map[gid]
                    else:
                        new_map[gid] = id
                mapid = new_map
                indices = [aliases[id] if id in aliases else id for id in indices]
                
                        
            
            # aggregation uses internal ids as unicity of scene_labels is not guarantee (eg if several scenes have been mixed)
            if aggregate:
                #compute sums for area integrated variables
                res = dict([(k, _agregate(output[k],indices)) for k in ['Eabs','Einc','EincSup','EincInf','Area', 'label']])
                # compute mean fluxes
                res['Eabsm2'] = dict([(k,res['Eabs'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k,0) for k in res['Eabs'].iterkeys()  ])
                res['Ei'] = dict([(k,(res['EincInf'][k] + res['EincSup'][k]) / res['Area'][k]) if res['Area'][k] > 0 else (k,0) for k in res['EincInf'].iterkeys()])
                res['EiInf'] = dict([(k,res['EincInf'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k,0) for k in res['EincInf'].iterkeys()])
                res['EiSup'] = dict([(k,res['EincSup'][k] / res['Area'][k]) if res['Area'][k] > 0 else (k,0) for k in res['EincSup'].iterkeys()])
            else: 
                res = dict([(k, _agregate(output[k],indices,list)) for k in output.keys()])
                
            #re-index results if mapid is given
            if mapid is not None:# empty mapid (corrresponding to absence of a list of shapes in the scene) should pass this test. Only none default options should skip and return all res
                for var in res.keys():
                    res[var] = dict([(k,(res[var])[v]) for k,v in mapid.items()])
                if len(res[res.keys()[0]]) <= 0:#pas de res trouve pour les mapid en entree
                    res={}
        
        return(res)


