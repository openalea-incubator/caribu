from copy import copy


def addSoil(caribuscene,_copy = True):
    '''    Add a soil along with the pattern of a CaribuScene (Supposing the pattern is aligned with coordinate axis) 
    '''
    
    if _copy:
        cs = copy(caribuscene)
    else:
        cs = caribuscene
    
    ids = cs.addSoil()
    
    return cs,ids
    
