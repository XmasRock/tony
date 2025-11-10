import requests
import sounddevice as sd
import numpy as np
import whisper
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.chains import LLMChain
import time
import json
import os

# --- Configuration ---
MCP_AUDIO_FILE = "/app/data/audio/voice_command.wav"
SAMPLE_RATE = 16000
RECORD_SECONDS = 5
N8N_COMMAND_WEBHOOK = "http://raspberrypi:5678/webhook/jetson_command"

# Ollama local (Jetson)
LLM_MODEL = "llama3"  # ou "mistral", "phi3", selon ce que tu as chargé avec Ollama

# --- Initialisation Whisper ---
whisper_model = whisper.load_model("base")

# --- Initialisation LLM LangChain ---
template = """
Tu es un assistant embarqué dans un Jetson Orin. 
Ton rôle est d'interpréter des commandes vocales humaines et de les traduire en JSON simple.

Voici quelques exemples :
- "redémarre le micro" -> {{"command": "restart_agent", "target": "audio"}}
- "redémarre la caméra" -> {{"command": "restart_agent", "target": "camera"}}
- "éteins-toi" -> {{"command": "shutdown"}}
- "redémarre-toi" -> {{"command": "reboot"}}

Commande à interpréter : "{user_input}"

Réponds UNIQUEMENT en JSON.
"""

prompt = PromptTemplate(template=template, input_variables=["user_input"])
llm = Ollama(model=LLM_MODEL)
chain = LLMChain(prompt=prompt, llm=llm)

# --- Fonctions ---

def record_audio(filename=MCP_AUDIO_FILE, duration=RECORD_SECONDS):
    """Enregistre la voix depuis le micro."""
    print("🎙️ Parlez maintenant...")
    data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    sd.play(np.zeros(1000))  # petit "clic" silence pour éviter un bruit résiduel
    import wave
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())
    print(f"✅ Audio enregistré : {filename}")
    return filename

def transcribe_audio(filename):
    """Transcrit l'audio en texte."""
    result = whisper_model.transcribe(filename, language="fr")
    text = result["text"].strip()
    print(f"🗣️ Transcription : {text}")
    return text

def interpret_command(text):
    """Envoie le texte au LLM pour extraire une commande JSON."""
    response = chain.run(user_input=text)
    print(f"🤖 Interprétation brute : {response}")
    try:
        cmd = json.loads(response)
        return cmd
    except json.JSONDecodeError:
        print("⚠️ Erreur : sortie LLM non JSON.")
        return None

def send_command_to_n8n(command_dict):
    """Envoie la commande à n8n via le webhook."""
    try:
        resp = requests.post(N8N_COMMAND_WEBHOOK, json=command_dict)
        print(f"📡 Commande envoyée à n8n : {command_dict}")
        print(f"✅ Réponse n8n : {resp.text}")
    except Exception as e:
        print(f"⚠️ Erreur d’envoi : {e}")

def voice_command_loop():
    """Boucle principale de commande vocale."""
    print("🎧 Agent de commande vocale actif. Dites une commande (Ctrl+C pour quitter).")
    while True:
        try:
            filename = record_audio()
            text = transcribe_audio(filename)
            if text:
                cmd = interpret_command(text)
                if cmd:
                    send_command_to_n8n(cmd)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt de l’agent vocal.")
            break
        except Exception as e:
            print(f"⚠️ Erreur dans la boucle : {e}")
            time.sleep(5)

if __name__ == "__main__":
    voice_command_loop()
