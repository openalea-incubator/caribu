#!/bin/bash

scons  prefix=${PREFIX} install

${PYTHON} setup.py install --prefix=${PREFIX} 
