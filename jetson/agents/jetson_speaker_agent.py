import os
import time
import json
import requests
from queue import Queue
from threading import Thread
from gtts import gTTS
import tempfile

# --- Configuration ---
QUEUE_FILE = "/app/data/speaker_queue.json"
N8N_SPEAKER_WEBHOOK = "http://raspberrypi:5678/webhook/speaker_feedback"
DEFAULT_LANG = "fr"     # langue par défaut
DEFAULT_VOLUME = 100    # 100 = normal, 150 = fort, 50 = faible

# --- Gestion de la file d’attente ---
def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def add_to_queue(item):
    """Ajoute un texte (et ses paramètres) à la file."""
    queue = load_queue()
    queue.append(item)
    save_queue(queue)
    print(f"📥 Ajouté à la file vocale : {item}")

def speak_text(text, volume=DEFAULT_VOLUME, lang=DEFAULT_LANG):
    """Prononce un texte avec gTTS et contrôle du volume via mpg123."""
    print(f"🗣️ Lecture : '{text}' (lang={lang}, volume={volume}%)")
    try:
        # Création du fichier audio temporaire
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            mp3_path = tmpfile.name
            tts.save(mp3_path)

        # Conversion du volume en facteur pour mpg123
        factor = int(max(10, min(volume, 200)) * 10)
        os.system(f"mpg123 -q -f {factor} {mp3_path}")

        os.remove(mp3_path)
        try:
            requests.post(N8N_SPEAKER_WEBHOOK, json={"status": "spoken", "text": text})
        except Exception:
            pass
    except Exception as e:
        print(f"❌ Erreur pendant la lecture : {e}")

def process_queue():
    """Boucle qui lit et vide la file d’attente."""
    while True:
        queue = load_queue()
        if queue:
            item = queue.pop(0)
            save_queue(queue)

            # Lecture d’un item (dict ou texte simple)
            if isinstance(item, dict):
                text = item.get("text", "")
                volume = item.get("volume", DEFAULT_VOLUME)
                lang = item.get("lang", DEFAULT_LANG)
            else:
                text, volume, lang = item, DEFAULT_VOLUME, DEFAULT_LANG

            if text:
                speak_text(text, volume, lang)
        else:
            time.sleep(2)

def run_server():
    """Serveur Flask pour recevoir du texte depuis n8n ou un autre agent."""
    from flask import Flask, request, jsonify
    app = Flask(__name__)

    @app.route("/speak", methods=["POST"])
    def speak():
        data = request.get_json(force=True)
        text = data.get("text")
        volume = data.get("volume", DEFAULT_VOLUME)
        lang = data.get("lang", DEFAULT_LANG)

        if not text:
            return jsonify({"status": "error", "message": "Aucun texte fourni"}), 400

        add_to_queue({"text": text, "volume": volume, "lang": lang})
        return jsonify({"status": "ok", "message": f"Texte ajouté à la file : {text}"}), 200

    print("🔊 Serveur Speaker (gTTS) prêt sur http://0.0.0.0:5051/speak")
    app.run(host="0.0.0.0", port=5051)

if __name__ == "__main__":
    # Lancement du lecteur et du serveur simultanément
    Thread(target=process_queue, daemon=True).start()
    run_server()
