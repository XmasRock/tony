import cv2
import face_recognition
import numpy as np
import websockets
import asyncio
import json
import os
from datetime import datetime

SERVER_WS = os.getenv("SERVER_WS", "ws://localhost:8000/mcp/ws")
KNOWN_FACES_DIR = "/app/data/known_faces"
TOLERANCE = 0.45

async def send_event(event_type, payload):
    async with websockets.connect(SERVER_WS) as ws:
        msg = {"type": event_type, "payload": payload}
        await ws.send(json.dumps(msg))

def load_known_faces():
    known_faces = []
    known_names = []
    for name in os.listdir(KNOWN_FACES_DIR):
        path = os.path.join(KNOWN_FACES_DIR, name)
        if not os.path.isfile(path):
            continue
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_faces.append(encodings[0])
            known_names.append(os.path.splitext(name)[0])
    return known_faces, known_names

async def main():
    known_faces, known_names = load_known_faces()
    print(f"✅ {len(known_faces)} visages connus chargés")

    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("❌ Impossible d'accéder à la caméra")
        return

    while True:
        ret, frame = video.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for encoding, loc in zip(encodings, locations):
            matches = face_recognition.compare_faces(known_faces, encoding, TOLERANCE)
            name = "Inconnu"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

            y1, x2, y2, x1 = loc
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            event = {
                "timestamp": datetime.now().isoformat(),
                "person": name,
                "bbox": [x1, y1, x2, y2],
            }
            await send_event("camera.person_detected", event)

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
