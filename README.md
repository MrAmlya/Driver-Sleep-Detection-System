# Driver Drowsiness Detection System

Real-time drowsiness detection using a webcam. The app detects eye closure and yawning, shows warnings on screen, and plays an alarm after continued drowsiness.

## How It Works

The main program is `drowsiness_detection.py`. It uses:

- OpenCV (`cv2`) to read webcam frames and draw text on the video.
- MediaPipe Face Mesh to detect facial landmarks.
- SciPy to calculate Euclidean distances between landmark points.
- Pygame to play `alarm.mp3` when drowsiness continues.

The app starts the webcam with `cv2.VideoCapture(0)`, reads each frame, resizes it to `800x600`, converts it from BGR to RGB, and sends it to MediaPipe Face Mesh. MediaPipe returns normalized face landmark coordinates, so the code converts each landmark into pixel coordinates using the frame width and height.

### Eye Aspect Ratio

EAR means Eye Aspect Ratio. It estimates how open or closed an eye is.

The code uses six landmarks for each eye:

```python
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
```

For each eye, the formula is:

```text
EAR = (vertical_distance_1 + vertical_distance_2) / (2 * horizontal_distance)
```

In code:

```python
v1 = distance.euclidean(eye[1], eye[5])
v2 = distance.euclidean(eye[2], eye[4])
h = distance.euclidean(eye[0], eye[3])
ear = (v1 + v2) / (2.0 * h)
```

When the eye is open, the vertical distances are larger, so EAR is higher. When the eye closes, the vertical distances shrink, so EAR becomes lower. The app averages both eyes:

```python
ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
```

If `ear < 0.25`, the app treats the driver as potentially drowsy.

### Mouth Aspect Ratio

MAR means Mouth Aspect Ratio. It estimates how open the mouth is, which helps detect yawning.

The code uses six mouth landmarks:

```python
MOUTH = [61, 291, 13, 14, 78, 308]
```

The formula is:

```text
MAR = vertical_mouth_distance / horizontal_mouth_distance
```

In code:

```python
v = distance.euclidean(mouth[2], mouth[3])
h = distance.euclidean(mouth[0], mouth[1])
mar = v / h
```

When the mouth opens wide, the vertical distance grows, so MAR becomes higher. If `mar > 0.75`, the app treats it as yawning.

### Drowsiness Logic

The app checks both signals on every frame:

- If `EAR < 0.25`, eyes are considered closed.
- If `MAR > 0.75`, yawning is detected.
- If either condition is true, `counter` increases.
- If drowsiness continues for `20` frames, the app displays `WAKE UP!` and plays `alarm.mp3`.
- If the driver looks active again, `counter` resets to `0` and the alarm stops.

The thresholds are defined near the top of the code:

```python
EAR_THRESHOLD = 0.25
MAR_THRESHOLD = 0.75
FRAME_THRESHOLD = 20
```

These values are simple demo thresholds. They may need adjustment depending on lighting, camera angle, face distance, and the person using the system.

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
