"""
Real‑time face‐and‐eye detection with OpenCV.

Dependencies
------------
1. Python ≥ 3.8
2. opencv‑python  (pip install opencv-python)

Run
---
python detect_face_and_eyes.py
Press the `q` key to quit the preview window.
"""
import cv2
import sys
from pathlib import Path

# ------------------------------------------------------------------
# 1) Load the Haar‑cascade classifiers that ship with OpenCV
#    (They’re small XML files containing the trained models.)
# ------------------------------------------------------------------
cascade_dir = Path(cv2.data.haarcascades)            # built‑in path
face_cascade = cv2.CascadeClassifier(str(cascade_dir / "haarcascade_frontalface_default.xml"))
eye_cascade  = cv2.CascadeClassifier(str(cascade_dir / "haarcascade_eye.xml"))

if face_cascade.empty() or eye_cascade.empty():
    sys.exit("❌ Couldn’t load the Haar cascade files. Check OpenCV install.")

# ------------------------------------------------------------------
# 2) Open the default laptop webcam (device 0)
# ------------------------------------------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)             # CAP_DSHOW avoids some Windows lag; harmless on Linux/macOS
if not cap.isOpened():
    sys.exit("❌ Cannot access the webcam.")

print("✅ Webcam stream started. Press 'q' to quit.")

# ------------------------------------------------------------------
# 3) Main loop: capture → detect → annotate → display
# ------------------------------------------------------------------
while True:
    ret, frame = cap.read()                          # Grab one frame
    if not ret:
        print("⚠️  Frame capture failed, trying again...")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # Haar cascades work on grayscale

    # ---- Detect faces in the frame --------------------------------
    faces = face_cascade.detectMultiScale(
        gray,              # input image (grayscale)
        scaleFactor=1.1,   # search for faces at 10% size increments
        minNeighbors=5,    # how many “neighbor” rectangles each candidate needs to be retained
        minSize=(60, 60)   # ignore tiny faces that are likely noise
    )

    # ---- Draw rectangles around faces and then eyes --------------
    for (x, y, w, h) in faces:
        # Face rectangle (green)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Region Of Interest (ROI) for eyes – limits search area
        roi_gray  = gray[y:y + h,  x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(20, 20)
        )

        for (ex, ey, ew, eh) in eyes:
            # Eye rectangle (red)
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    # ---- Show the annotated frame --------------------------------
    cv2.imshow("Face & Eye Detection – press 'q' to quit", frame)

    # ---- Exit if the user presses the `q` key ---------------------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------------------------------------------------------
# 4) Clean up – release camera and close window
# ------------------------------------------------------------------
cap.release()
cv2.destroyAllWindows()
