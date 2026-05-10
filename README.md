# Driver Drowsiness Detection System

Real-time drowsiness detection using a webcam. The app detects eye closure and yawning, shows warnings on screen, and plays an alarm after continued drowsiness.

## Requirements

- Python 3.10, 3.11, or 3.12
- Webcam access
- `alarm.mp3` in the project folder

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python drowsiness_detection.py
```

Press `q` in the webcam window to quit.

## Clickable Launchers

- macOS: double-click `run_drowsiness_detection.command`
- Windows: double-click `run_drowsiness_detection.bat`

To create a Windows `.exe`, run `build_windows_exe.bat` on Windows. The output will be created at `dist\DriverDrowsinessDetection.exe`.

If Windows shows an error about `.venv\Scripts\activate` or `module 'mediapipe' has no attribute 'solutions'`, delete the `.venv` folder and run the `.bat` file again. If dependency installation fails on `mediapipe`, install Python 3.10, 3.11, or 3.12 from python.org and make sure Python is added to PATH.

## Files

- `drowsiness_detection.py` - main application
- `requirements.txt` - Python dependencies
- `alarm.mp3` - alarm sound file, required for audio alert
- `run_drowsiness_detection.command` - macOS launcher
- `run_drowsiness_detection.bat` - Windows launcher
- `build_windows_exe.bat` - Windows EXE builder

## Note

This project is for learning/demo purposes and should not be used as the only safety system while driving.
