REM - Install miniconda if necessary.
call %~dp0\setup\miniconda_install.bat

REM - Create Conda Environment if necessary
call %~dp0\setup\environment_create.bat
