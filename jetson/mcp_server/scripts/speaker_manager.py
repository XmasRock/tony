import os
import subprocess
from gtts import gTTS
from datetime import datetime

DATA_DIR = "/app/data/speaker"
os.makedirs(DATA_DIR, exist_ok=True)

def say(text: str, lang="fr"):
    """Convertit un texte en audio et le joue sur le haut-parleur Bluetooth."""
    tts = gTTS(text=text, lang=lang)
    audio_file = os.path.join(DATA_DIR, f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
    tts.save(audio_file)
    try:
        subprocess.run(["bluetoothctl", "connect", "$(cat /app/config/bluetooth_mac.txt)"], check=False)
        subprocess.run(["mpg123", audio_file], check=True)
        print(f"🔊 Lecture: {text}")
    except Exception as e:
        print(f"Erreur lecture audio: {e}")
    return audio_file
