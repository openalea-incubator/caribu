#!/bin/bash

scons install --build_prefix=${BUILD_PREFIX} --prefix=${PREFIX} 

${PYTHON} setup.py install --prefix=${PREFIX} 
