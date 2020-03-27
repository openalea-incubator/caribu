COPY options_conda_win.py options.py

REM systeminfo

scons -j %CPU_COUNT% 
%PYTHON% setup.py install
scons install 

if errorlevel 1 exit 1

