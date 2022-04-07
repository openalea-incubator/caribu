#scons parameters file
#use this file to pass custom parameter to SConstruct script
import platform

if platform.system() == 'Windows':
    compiler = 'mingw'
