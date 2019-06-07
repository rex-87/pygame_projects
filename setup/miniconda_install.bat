REM - This script will download miniconda from the official url and (silently) install it in the user profile directory.
REM - If already installed, this script will not do anything.
REM - Please note that the 32-bit version of miniconda is used, this is because ATK is tied to 32-bit DLLs (Ate2SmComms, ...)
REM - Details:
REM -    https://conda.io/projects/conda/en/latest/user-guide/install/windows.html#install-win-silent
IF NOT EXIST %UserProfile%\miniconda3 (
	@echo on
	echo Downloading Miniconda in %UserProfile%\Downloads ...
	powershell -Command "Invoke-WebRequest https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile %UserProfile%\Downloads\Miniconda3-latest-Windows-x86_64.exe"
	echo Please wait while Miniconda is installed in %UserProfile%\miniconda3_x86_64 ...
	call %UserProfile%\Downloads\Miniconda3-4.6.14-Windows-x86.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\miniconda3
)
