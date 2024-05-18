#!/bin/bash

scons install --prefix=${PREFIX} 

${PYTHON} setup.py install --prefix=${PREFIX} 
