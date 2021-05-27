COPY options_conda_win.py options.py

REM systeminfo

REM scons -j %CPU_COUNT% install

%PYTHON% setup.py install

if errorlevel 1 exit 1

