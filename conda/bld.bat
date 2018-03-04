%PYTHON% setup.py build_ext --scons-ext-param=" compiler='mingw' " install

if errorlevel 1 exit 1
