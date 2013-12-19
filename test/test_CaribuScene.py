from alinea.caribu.CaribuScene import CaribuScene
import os

def test_tutorial():
    """ test of simple call to caribu, as in visualea tutorial
    """
    scene = "../src/caribu/data/f331s1_100plantes.can"
    light  = "../src/caribu/data/zenith.light"
    pattern = "../src/caribu/data/filter.8"
    opt="../src/caribu/data/opt/"
    resultatWaveL = {}
    for i in os.listdir(opt):
        if len(os.path.basename(opt+i).split('.')[1]) <= 3:
            c_scene = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt+i)
            output = c_scene.runCaribu(infinity=True)
            resultatWaveL[os.path.basename(opt+i).split('.')[0]] = output
    return(c_scene, resultatWaveL)
    
def test_tutorialBeta():
    """ test of simple call to caribu, as in visualea tutorial
    """
    scene = "../src/caribu/data/essai.can"
    light  = "../src/caribu/data/zenith.light"
    pattern = "../src/caribu/data/filter.8"
    opt = "../src/caribu/data/par.opt"
    c_scene = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt)
    output = c_scene.runCaribu(infinity=True)
    return(c_scene, output)

def test_getOptical():
    cs, out = test_tutorialBeta()
    opts = cs.getOptical()
   # assert opts[0] == (0.1,0.05,0.1,0.05)
    return opts
    
def test_getNormals():
    cs, out = test_tutorialBeta()
    norms = cs.getNormals()
    #assert opts[0] == (0.1,0.05,0.1,0.05)
    return norms
  
def test_getCenters():
    cs, out = test_tutorialBeta()
    centers = cs.getCenters()
    return centers
    
def test_getDistance():
    cs, out = test_tutorialBeta()
    distance = cs.getDistance()
    return distance
    
def test_getNorms():
    cs, out = test_tutorialBeta()
    norms = cs.getNormsAll()
    return norms
    
def test_prodScal():
    from alinea.caribu.caribu import vcaribu
    from alinea.caribu.label import Label
    from openalea.plantgl.all import Vector3
    import numpy as np
    import math
    
    # ********************
        #first test with the camera normal (camera see like light)
    # ********************
    
    camera = Vector3(0,0,-1)
   
        # ****
            #FilterT.can
        # ****      
   
    #scene = "../src/caribu/data/filterT.can"
    #pattern = "../src/caribu/data/filter.8" #limit of the scene and allow to infinity
    
        # ****
            #1200_normal.can
        # ****  
    scene = "../src/caribu/data/1200_normal_9-12-13.can"
    pattern = "../src/caribu/data/density04_9-12-13.8"
    
    opt = "../src/caribu/data/par.opt"
    
        # ****
            #light  = "../src/caribu/data/zenith.light"  ==  position of the camera in space (1 0 0 -1), nadir position
        # **** 
        
    light  = "../src/caribu/data/zenith.light"    
    cs = CaribuScene(scene=scene, light=light, opt=opt) #delete pattern for avoid to take a small triangle with an area of the order 10^(-6)
    out_camera = cs.runCaribu(infinity=False) 

        # ****
            #Filter little triangle : Area > 1e-6
        # ****        

    out_cam_area = []
    for i in range(len(out_camera["Area"])):
        if float(out_camera["Area"][i]) > 0.000001:
            temp = [out_camera["EiSup"][i], out_camera["EiInf"][i], out_camera["label"][i], i]
            out_cam_area.append(temp)
    
        # ****
            #reflecNulle allows of know visible triangles
        # ****    
    
    normals = cs.getNormals() 
    numero_ligne = [] #allow to write visible triangle in out file
    reflecNulle = {} #key = numero of the triangle, values = [0] 0 if the triangle is invisible for the camera else 1
                                                            #[1] if value[0] == 1 the dot product of camera with the normal of triangle
                                                                     
    for i in range(len(out_cam_area)): # i including between 0 at the length of the filter list of triangles
        if (out_cam_area[i][0] > 0.0 or out_cam_area[i][1] > 0.0): #threshold for the moment egal at 0.0        
            reflecNulle[i] = [1, np.vdot(camera,normals[out_cam_area[i][3]])]
            numero_ligne.append(out_cam_area[i][3])          
        else:
            reflecNulle[i] = [0,0]
        
    # ********************
        #second test with natural light for all wavelength
    # ******************** 
    
    file_list = "../src/caribu/data/wavelength/"
    #file_list = "../src/caribu/data/test/"
    light="../src/caribu/data/Turtle16soc.light"    
    opt_list = os.listdir(file_list)
    list_opt = [] #contain the list cleaned of optics files
    
        # ****
            # cleaning backup files with tilde ~ in their extension for avoid execute vcaribu above 
        # ****
    
    for i in opt_list:
        if len(os.path.basename(file_list+i).split('.')[1]) <= 3:
            list_opt.append(file_list+i)

        # ****
            # recover the max height
        # ****    
    
    centres = cs.getCenters()
    _,_,maxHei = centres[0]
    
    for z in centres:
        A,B,C = z
        if C > maxHei:
            maxHei = C
    
    print "maximum Height",str(maxHei)
    maxHei = maxHei + 2
    
    
    
        # ****
            # run vcaribu algorithm, take into account multi wavelength
                #optiondict: 
                    #Hc: Height can, heigth max of the canopie
                    #Nz: number of layers 
                    #infinity: allow to avoid side effect
                    #Ds: is the diameter of the radiosity sphere 
                    #1st: False allow to use the radiosity
        # ****      
                
    optiondict = {'Hc': maxHei, 'Nz': 10, 'infinity': True, 'Ds': 70, '1st': False}
    vcout,status = vcaribu(scene, light, list_opt, pattern, optiondict)
    
    print "Number of triangle in the first test",str(len(out_camera["EiSup"])),"\nNumber of triangle in the second test",str(len(vcout[vcout.keys()[0]]["data"]["Ei_sup"]))
    
    """
    #check if the label list of triangles between out_cam_area ans vcout is the same
    compt_diff = 0
    for i in range(len(out_cam_area)):
        if out_cam_area[i][2] != vcout["700"]["data"]["label"][i]:
            print out_cam_area[i][2],vcout["700"]["data"]["label"][i]
            compt_diff += 1 #any difference, all label are same
    print "len(out_cam_area)",len(out_cam_area)
    print "compt_diff",compt_diff
    """
    
    # ******************** 
        #build the file used for acp test, as many column as files
    # ********************
    
        # ****
            #compute the reflectance for all triangle taking into account the leaf species (green or senesente)
        # ****
   
    resultatWaveL = {} #stock the reflectance for all triangles for all wavelength
                       #key = wavelength , value = list of reflectance either visible triangles or all triangles
    
    label_specie = []    
    file_label_done = 0
    
    #length of triangles
    length_tri = []
    cs = CaribuScene(scene=scene, light=light, pattern=pattern, opt=opt) #allow to centers with the good list    
    centres = cs.getCenters()
    
    #tab for get the "id" of the triangles with the strange values
    val_strange = []
    
    
    
    _,eimax,_ = cs.getIncidentEnergy() # compute max value = sum of emmission of sources
    
    def _nan_to_zero(x):
        try:
            from math import isnan
        except:
             #to be back compatile with python 2.5
            def isnan(num):
                return num != num         
        return(0 if isnan(x) else x)
     
    for i in list_opt:
        nom_WL = os.path.basename(i).split('.')[0]
        d = vcout[nom_WL]['data']
                     
        i_ligne = 0       
        for k in d['Ei_inf']:    
            if math.isnan(k) == True or min(eimax,k) == eimax:
                if not i_ligne in val_strange: 
                    val_strange.append(i_ligne)
            i_ligne += 1
        i_ligne = 0
        
        for k in d['Ei_sup']:    
            if math.isnan(k) == True or min(eimax,k) == eimax:
                if not i_ligne in val_strange: 
                    val_strange.append(i_ligne)
            i_ligne += 1 
        #on ne doit pas juste mettre les val a 0 mais supprimer le spectre
    
    
    for i in list_opt:
        nom_WL = os.path.basename(i).split('.')[0]
        fd = open(i).readlines()
        reflectance = {}
        nombre_esp = 1
        for ligne in fd:
            if ligne[0] == "e":
                result = [0,0,0,0,0]
                spl = ligne.split()
                result[0] = float(spl[2]) #reflectance stem
                result[1] = float(spl[4]) #reflectance face Sup
                result[2] = float(spl[5]) #transmisttance face Sup
                result[3] = float(spl[7]) #reflectance face Inf
                result[4] = float(spl[8]) #transmisttance face Inf
                reflectance[nombre_esp] = result
                nombre_esp += 1
        
            # ****
                #filter nan values, negative values occuring in EiInf/EiSup and values > Eimax * 2 (reflectance diffuse)
            # ****
            
    
        
        
                
        result_output = [] #stock the reflectance for all triangle for one wavelength
        for j in reflecNulle.keys():
            if not j in val_strange:
                label_triangle =  Label(vcout[nom_WL]["data"]["label"][j]).optical_id
                feuille = Label(vcout[nom_WL]["data"]["label"][j]).is_leaf()                      
                
                #print feuille , Label(vcout[nom_WL]["data"]["label"][j])._get_transparency()
                          
                if feuille == True and reflecNulle[j][0] == 1:
                    if file_label_done == 0:
                        if label_triangle == 1:
                            label_specie.append("vert")
                        else:
                            label_specie.append("senescent")
                        
                        #length of triangles
                        _,_,C = centres[j]
                        length_tri.append(C)
                        
                        
                    if reflecNulle[j][1] >= 0.0: #take the face Inf for normal model and face Sup for ADEL model because ADEL reverse triangles
                    
                        result_output.append(float(vcout[nom_WL]["data"]["Ei_inf"][j]*reflectance[label_triangle][1]))
                        
                    else: #take the face Sup or face Inf for ADEL model
                    
                        result_output.append(float(vcout[nom_WL]["data"]["Ei_sup"][j]*reflectance[label_triangle][3]))
        if len(result_output) > 0:        
            resultatWaveL[nom_WL] = []
            resultatWaveL[nom_WL].extend(result_output)
        file_label_done = 1
       
        # ****
            #build file
        # ****    
               
    fiW = "R_ACP.csv"
    fiWrite = open(fiW, "w")
    
    wl_trier = [] #wavelength sort by ascending order
    for i in vcout.keys():
        wl_trier.append(int(i))
    
    tri_rapide2(wl_trier,0,len(wl_trier)-1)
    print wl_trier
    
    for i in range(len(resultatWaveL[str(wl_trier[0])])): #each column is a wavelength (variable) and each row is one triangle (ind)
        for key in wl_trier:  
            fiWrite.write(str(resultatWaveL[str(key)][i])+"\t")
        fiWrite.write(str(label_specie[i])+"\t") 
        fiWrite.write(str(length_tri[i]))   
        fiWrite.write("\n")
    fiWrite.close()

    # ********************
        #write a visible triangle in file
    # ********************
 
    fi = open(scene)
    fiRead = fi.readlines()
        
        # ****    
            #clean scene file => delete comments
        # ****
        
    for i in fiRead:
        if i[0] == "#":
            fiRead.remove(i)    
    fi.close()       

    fichW = "triangles_visible.can"
    fichTri = open(fichW, "w")
    for i in numero_ligne:
        fichTri.write(fiRead[i])
        
            
    return  vcout, out_camera
      
# ******************** ******************* #
      #END of test_prodScal() function
# ******************** ******************* #
    
def partitionner2(T, premier, dernier, pivot):
           

    temp = T[pivot]
    T[pivot] = T[dernier]
    T[dernier] = temp
    j = premier
    for i in range(premier, dernier):
        if T[i] <= T[dernier]:
            temp = T[i]
            T[i] = T[j]
            T[j] = temp
            j = j + 1
    temp = T[j]
    T[j] = T[dernier]
    T[dernier] = temp
    return j
    
def tri_rapide2(t, premier, dernier):
    import random as rd
    if premier < dernier:
        pivot = rd.randint(premier,dernier)
        pivot = partitionner2(t,premier, dernier,pivot)
        tri_rapide2(t,premier,pivot-1)
        tri_rapide2(t,pivot+1,dernier)   
     
    
    
    
    
