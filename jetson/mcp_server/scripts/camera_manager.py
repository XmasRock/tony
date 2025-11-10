import cv2
import os
import face_recognition
import numpy as np
from datetime import datetime

CAMERA_INDEX = 0
DATA_DIR = "/app/data/camera"
os.makedirs(DATA_DIR, exist_ok=True)

known_faces_dir = os.path.join(DATA_DIR, "known_faces")
os.makedirs(known_faces_dir, exist_ok=True)

def capture_image(filename=None):
    """Capture une image et la sauvegarde localement."""
    cam = cv2.VideoCapture(CAMERA_INDEX)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        raise RuntimeError("Impossible de capturer l'image depuis la caméra.")
    if filename is None:
        filename = os.path.join(DATA_DIR, f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    cv2.imwrite(filename, frame)
    return filename

def recognize_person():
    """Tente de reconnaître une personne connue à partir de la caméra."""
    frame_path = capture_image()
    unknown_image = face_recognition.load_image_file(frame_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if not unknown_encoding:
        return None
    unknown_encoding = unknown_encoding[0]

    # Charger les visages connus
    known_faces = []
    known_names = []
    for name in os.listdir(known_faces_dir):
        path = os.path.join(known_faces_dir, name)
        if os.path.isdir(path):
            for img_file in os.listdir(path):
                img_path = os.path.join(path, img_file)
                known_image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(known_image)
                if encodings:
                    known_faces.append(encodings[0])
                    known_names.append(name)

    if not known_faces:
        return None

    results = face_recognition.compare_faces(known_faces, unknown_encoding, tolerance=0.5)
    face_distances = face_recognition.face_distance(known_faces, unknown_encoding)
    best_match_index = np.argmin(face_distances)
    if results[best_match_index]:
        return known_names[best_match_index]
    return None
