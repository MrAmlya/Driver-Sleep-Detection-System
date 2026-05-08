@echo off
cd /d "%~dp0"

if not exist ".venv" (
    python -m venv .venv
)

call .venv\Scripts\activate

pip install -r requirements.txt
pip install pyinstaller

pyinstaller ^
    --onefile ^
    --name DriverDrowsinessDetection ^
    --add-data "alarm.mp3;." ^
    drowsiness_detection.py

echo.
echo Build complete.
echo EXE location: dist\DriverDrowsinessDetection.exe
echo.
pause
