@echo off
setlocal enabledelayedexpansion

:: Change directory to the one containing this batch file
cd /d "%~dp0"

:: Initialize an empty variable to hold the list of .whl files
set "whl_files="

:: Iterate over all .whl files and build the command
for %%f in (*.whl) do (
    set "whl_files=!whl_files! %%f"
)

:: Check if any .whl files were found
if "!whl_files!"=="" (
    echo No .whl files found in the directory.
    exit /b 1
)

:: Print the pip install command for debugging
echo pip install !whl_files!

:: Execute the pip install command
pip install !whl_files!

echo All installations are complete.
exit /b 0
