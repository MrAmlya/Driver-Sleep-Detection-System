# Driver Drowsiness Detection System

Real-time drowsiness detection using a webcam. The app detects eye closure and yawning, shows warnings on screen, and plays an alarm after continued drowsiness.

## Requirements

- 64-bit Python 3.12
- Webcam access
- `alarm.mp3` in the project folder

## macOS/Linux Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## macOS/Linux Run

```bash
python drowsiness_detection.py
```

Press `q` in the webcam window to quit.

## Windows Run

Use the launcher so Windows runs the app inside the project virtual environment:

```bat
run_drowsiness_detection.bat
```

If you run from PowerShell or Command Prompt manually, use:

```bat
.venv\Scripts\python.exe drowsiness_detection.py
```

Do not use `python drowsiness_detection.py` on Windows unless you have already activated `.venv`; otherwise Windows may use a different Python that does not have `cv2` installed.

## Clickable Launchers

- macOS: double-click `run_drowsiness_detection.command`
- Windows: double-click `run_drowsiness_detection.bat`

To create a Windows `.exe`, run `build_windows_exe.bat` on Windows. The output will be created at `dist\DriverDrowsinessDetection.exe`.

If Windows shows an error about `.venv\Scripts\activate` or `module 'mediapipe' has no attribute 'solutions'`, delete the `.venv` folder and run the `.bat` file again. If dependency installation fails on `mediapipe`, install 64-bit Python 3.12 from python.org and make sure Python is added to PATH.

## Windows Run Steps

1. Install 64-bit Python 3.12 from python.org.
2. Download or pull the latest project code.
3. Open the project folder, the folder that contains `drowsiness_detection.py`.
4. Delete the `.venv` folder if it already exists. Do not delete `.env`; this project uses `.venv`.
5. Double-click `run_drowsiness_detection.bat`.
6. Wait for dependencies to install. The webcam window should open after installation finishes.
7. Press `q` in the webcam window to quit.

Only run `build_windows_exe.bat` if you want to create a standalone `.exe`. It is not needed for normal project running.

## Files

- `drowsiness_detection.py` - main application
- `requirements.txt` - Python dependencies
- `alarm.mp3` - alarm sound file, required for audio alert
- `run_drowsiness_detection.command` - macOS launcher
- `run_drowsiness_detection.bat` - Windows launcher
- `build_windows_exe.bat` - Windows EXE builder

## Note

This project is for learning/demo purposes and should not be used as the only safety system while driving.
