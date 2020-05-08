scons -j ${CPU_COUNT} CC=$CC  CCFLAGS=$CCFLAGS install
$PYTHON setup.py install