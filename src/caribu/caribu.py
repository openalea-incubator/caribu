""" Chaine les appel de s2v, mcsail et canestra, comme le fait cpfg via caribu
    Syntaxe: caribu.csh Ds file.light file.can nz h file.8 file1.opt ... fileN.opt

  Exemple /home/tld/chelle/QHS/Calgary/dev/Canestra/MC-SAIL/Test 
  caribu.csh 0.2 sky2.light Tout.can 3 18 Tout.8 test nir par

  MC98
  C. Pradal - 2009
  MC09
  Contact: chelle@grinon.inra.fr
  INRA - INRIA - CIRAD
"""
import os
from subprocess import Popen,STDOUT, PIPE
import tempfile
import platform
from openalea.core.path import path

def _process(cmd, directory, out):
    """ 
    Run a process in a shell. 
    Return the outputs in a file or string.
    """
    #print ">> caribu.py: process(%s) called..."%(cmd)

    f = open(out,'w')
    if platform.system() == 'Darwin':
        p = Popen(cmd, shell=True, cwd=directory,
              stdin=PIPE, stdout=f, stderr=PIPE)
        status = p.communicate()
    else:
        p = Popen(cmd, shell=True, cwd=directory,
              stdin=PIPE, stdout=f, stderr=STDOUT)
        status = p.wait()

    f.close()
    
    #print "<<< caribu.py: process finished!"
    return status

def _safe_iter(obj, atomic_types = (basestring, int, float, complex)):
    """Equivalent to iter when obj is iterable and not defined as atomic.
    If obj is defined atomic or found to be not iterable, returns iter((obj,)).
    safe_iter(None) returns an empty iterator"""
    if not isinstance(obj, atomic_types):
        try:
            return iter(obj)
        except TypeError:
            pass
    return iter((obj,) * (obj is not None))

def _abrev(fnc,maxlg=1):
    """
    abreviate a text string containing a path or a file content to the first maxlg lines,

