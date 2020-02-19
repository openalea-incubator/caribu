COPY options_conda_win.py options.py

REM systeminfo

scons -j %CPU_COUNT% 
REM MOVE build-scons\bin\* $PREFIX\bin
REM MOVE build-scons\lib\* $PREFIX\lib

%PYTHON% setup.py install

if errorlevel 1 exit 1

