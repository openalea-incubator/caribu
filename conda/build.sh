scons -j ${CPU_COUNT} CC=$CC  CCFLAGS=$CCFLAGS
mv build-scons/bin/* $PREFIX/bin
mv build-scons/lib/* $PREFIX/lib
#mkdir $PREFIX/include/caribu
#mv build-scons/include/* $PREFIX/include/caribu
$PYTHON setup.py install