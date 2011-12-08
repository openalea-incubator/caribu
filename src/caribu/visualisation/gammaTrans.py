from math import *

def gammaTrans(values, gamma=1,minval =None,maxval=None):
    '''    return value normalised and raised at exponent gamma
    '''
    if minval is None:
        m = min(values)
    else:
        m = minval
    if maxval is None:
        M = max(values)
    else:
        M = maxval
    if (m == M) :
        norm = 1
    else:
        norm = M - m
    res = map(lambda(x): ((x - m) / float(norm))**gamma,values) 
    # write the node code here.

    # return outputs
    return res,
