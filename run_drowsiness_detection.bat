@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="

py -3.12 -c "import sys" >nul 2>nul
if not errorlevel 1 set "PYTHON_EXE=py -3.12"

if not defined PYTHON_EXE (
    py -3.11 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=py -3.11"
)

if not defined PYTHON_EXE (
    py -3.10 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=py -3.10"
)

if not defined PYTHON_EXE (
    python -c "import sys; raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=python"
)

if not defined PYTHON_EXE (
    echo Python 3.10, 3.11, or 3.12 was not found.
    echo Install one of those versions from https://www.python.org/downloads/windows/
    echo Make sure "Add python.exe to PATH" is selected during installation.
    pause
    exit /b 1
)

if not exist ".venv" (
    %PYTHON_EXE% -m venv .venv
    if errorlevel 1 (
        echo Failed to create the virtual environment.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment activation script was not found.
    echo Delete the .venv folder and run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment Python was not found.
    echo Delete the .venv folder and run this file again.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if (3, 10) <= sys.version_info[:2] <= (3, 12) else 1)" >nul 2>nul
if errorlevel 1 (
    echo Existing virtual environment uses an unsupported Python version.
    echo Delete the .venv folder and run this file again with Python 3.10, 3.11, or 3.12 installed.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo If this mentions mediapipe, use Python 3.10, 3.11, or 3.12 and run this file again.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" drowsiness_detection.py
if errorlevel 1 (
    echo The application stopped with an error.
)

pause
