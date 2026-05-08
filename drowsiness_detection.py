import cv2
import mediapipe as mp
from scipy.spatial import distance
import pygame

# -----------------------------
# ALARM SETUP
# -----------------------------
ALARM_SOUND = "alarm.mp3"
alarm_available = False

try:
    pygame.mixer.init()
    alarm_available = True
except pygame.error as error:
    print(f"Audio unavailable. Alarm will be disabled: {error}")

# -----------------------------
# MEDIAPIPE SETUP
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# EYE LANDMARKS
# -----------------------------
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# -----------------------------
# MOUTH LANDMARKS (YAWN DETECTION)
# -----------------------------
MOUTH = [61, 291, 13, 14, 78, 308]

# -----------------------------
# THRESHOLDS
# -----------------------------
EAR_THRESHOLD = 0.25
MAR_THRESHOLD = 0.75
FRAME_THRESHOLD = 20

counter = 0
alarm_on = False

# -----------------------------
# EAR FUNCTION (EYES)
# -----------------------------
def eye_aspect_ratio(eye):
    v1 = distance.euclidean(eye[1], eye[5])
    v2 = distance.euclidean(eye[2], eye[4])
    h = distance.euclidean(eye[0], eye[3])
    return (v1 + v2) / (2.0 * h)

# -----------------------------
# MAR FUNCTION (MOUTH)
# -----------------------------
def mouth_aspect_ratio(mouth):
    v = distance.euclidean(mouth[2], mouth[3])
    h = distance.euclidean(mouth[0], mouth[1])
    return v / h

# -----------------------------
# CAMERA START
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam. Check camera permissions or connection.")
    if alarm_available:
        pygame.mixer.quit()
    raise SystemExit(1)

print("Driver Drowsiness System Started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 600))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            left_eye = []
            right_eye = []
            mouth = []

            # ---------------- EYE POINTS ----------------
            for idx in LEFT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))

            for idx in RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))

            # ---------------- MOUTH POINTS ----------------
            for idx in MOUTH:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                mouth.append((x, y))

            # ---------------- CALCULATIONS ----------------
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
            mar = mouth_aspect_ratio(mouth)

            # DISPLAY VALUES
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # ---------------- DROWSINESS LOGIC ----------------
            drowsy = False

            if ear < EAR_THRESHOLD:
                drowsy = True

            if mar > MAR_THRESHOLD:
                drowsy = True
                cv2.putText(frame, "YAWNING DETECTED!", (200, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 165, 255), 3)

            if drowsy:
                counter += 1
                cv2.putText(frame, "DROWSINESS WARNING!", (180, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

                if counter >= FRAME_THRESHOLD:
                    cv2.putText(frame, "WAKE UP!", (250, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

                    if alarm_available and not alarm_on:
                        try:
                            pygame.mixer.music.load(ALARM_SOUND)
                            pygame.mixer.music.play()
                            alarm_on = True
                        except pygame.error as error:
                            print(f"Could not play alarm sound: {error}")

            else:
                counter = 0
                if alarm_available and alarm_on:
                    pygame.mixer.music.stop()
                    alarm_on = False

                cv2.putText(frame, "ACTIVE", (250, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if alarm_available:
    pygame.mixer.quit()
