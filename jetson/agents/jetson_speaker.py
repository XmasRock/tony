# /jetson/agents/jetson_speaker.py

import time
import requests
from scripts import speaker_manager
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

# Webhook n8n qui peut envoyer des phrases à prononcer
N8N_SPEAKER_ENDPOINT = "http://raspberrypi:5678/webhook/speaker_output"

# Ollama local pour reformuler les phrases si besoin
llm = Ollama(model="llama3", base_url="http://localhost:11434")

reformulation_prompt = PromptTemplate.from_template("""
Tu es la voix de l'assistant de Valérie.
Réécris cette phrase pour qu'elle soit naturelle, chaleureuse et fluide à dire à voix haute :
"{phrase}"
""")

def speak_loop():
    print("🔊 Agent speaker LangChain actif...")
    while True:
        try:
            # Vérifie si n8n a envoyé un message à lire
            response = requests.get(N8N_SPEAKER_ENDPOINT, timeout=10)
            if response.status_code == 200:
                text = response.json().get("text", "")
                if text.strip():
                    # Reformule la phrase pour une meilleure oralité
                    refined = llm.invoke(reformulation_prompt.format(phrase=text))
                    print(f"🗣️ Lecture : {refined}")
                    speaker_manager.say(refined)
            time.sleep(5)

        except Exception as e:
            print(f"⚠️ Erreur agent speaker : {e}")
            time.sleep(10)

if __name__ == "__main__":
    speak_loop()
