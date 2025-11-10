import os
import time
import json
import requests
import pyttsx3
from queue import Queue
from threading import Thread

# --- Configuration ---
QUEUE_FILE = "/app/data/speaker_queue.json"
N8N_SPEAKER_WEBHOOK = "http://raspberrypi:5678/webhook/speaker_feedback"

# --- Initialisation du moteur TTS ---
engine = pyttsx3.init()
engine.setProperty('rate', 180)   # vitesse de parole
engine.setProperty('volume', 1.0) # volume max
voices = engine.getProperty('voices')

# Sélection d'une voix française si disponible
for voice in voices:
    if "french" in voice.name.lower() or "fr" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

# --- Gestion de la file d’attente ---
def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_queue(queue):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def add_to_queue(text):
    queue = load_queue()
    queue.append(text)
    save_queue(queue)
    print(f"📥 Ajouté à la file vocale : {text}")

def speak_text(text):
    """Prononce un texte avec pyttsx3."""
    print(f"🗣️ Lecture : {text}")
    engine.say(text)
    engine.runAndWait()
    try:
        requests.post(N8N_SPEAKER_WEBHOOK, json={"status": "spoken", "text": text})
    except:
        pass

def process_queue():
    """Boucle qui lit et vide la file d’attente."""
    while True:
        queue = load_queue()
        if queue:
            text = queue.pop(0)
            save_queue(queue)
            speak_text(text)
        else:
            time.sleep(2)

def run_server():
    """Petit serveur Flask pour recevoir du texte à lire depuis n8n ou un autre agent."""
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route("/speak", methods=["POST"])
    def speak():
        data = request.get_json()
        text = data.get("text")
        if not text:
            return jsonify({"status": "error", "message": "Aucun texte fourni"}), 400
        add_to_queue(text)
        return jsonify({"status": "ok", "message": f"Texte ajouté à la file : {text}"}), 200

    print("🔊 Serveur Speaker prêt sur http://0.0.0.0:5051/speak")
    app.run(host="0.0.0.0", port=5051)

if __name__ == "__main__":
    # Lancement du lecteur et du serveur simultanément
    Thread(target=process_queue, daemon=True).start()
    run_server()
