from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from scripts import audio_manager, speaker_manager, memory_manager
import requests
import time

# Ollama modèle local
llm = Ollama(model="llama3", base_url="http://localhost:11434")

# Mémoire conversationnelle persistante
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Chaîne de conversation LangChain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

N8N_WEBHOOK = "http://raspberrypi:5678/webhook/audio_trigger"

def listen_and_chat(person="Inconnu"):
    print(f"🎙️ Agent LangChain audio actif pour {person}...")
    while True:
        try:
            wav_path = audio_manager.record_audio(duration=5)
            text = audio_manager.transcribe_audio(wav_path)
            if not text.strip():
                continue

            print(f"👂 Entrée utilisateur : {text}")

            # Génère une réponse avec le contexte
            response = conversation.predict(input=text)

            print(f"💬 Réponse : {response}")

            # Sauvegarde dans la mémoire persistante
            memory_manager.save_message(person, "user", text)
            memory_manager.save_message(person, "assistant", response)

            # Option : envoyer à n8n pour orchestration
            requests.post(N8N_WEBHOOK, json={"person": person, "text": text, "response": response})

            # Parle la réponse
            speaker_manager.say(response)

        except Exception as e:
            print(f"⚠️ Erreur LangChain audio : {e}")
            time.sleep(5)

if __name__ == "__main__":
    listen_and_chat()
