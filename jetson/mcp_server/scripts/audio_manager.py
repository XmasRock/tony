import sounddevice as sd
import numpy as np
import wavio
import os
from datetime import datetime
import subprocess

DATA_DIR = "/app/data/audio"
os.makedirs(DATA_DIR, exist_ok=True)

SAMPLE_RATE = 16000
DURATION = 5  # secondes

def record_audio(filename=None, duration=DURATION):
    """Enregistre un court extrait audio depuis le micro."""
    if filename is None:
        filename = os.path.join(DATA_DIR, f"record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
    print("🎙️ Enregistrement...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    wavio.write(filename, recording, SAMPLE_RATE, sampwidth=2)
    print("✅ Enregistrement terminé :", filename)
    return filename

def transcribe_audio(file_path):
    """Transcrit un fichier audio avec Ollama (ou Whisper local)."""
    try:
        result = subprocess.run(
            ["whisper", file_path, "--model", "base", "--language", "fr"],
            capture_output=True,
            text=True
        )
        transcript = result.stdout.strip()
        return transcript
    except Exception as e:
        return f"Erreur de transcription: {e}"
