from scripts import audio_manager, memory_manager
import requests
import time

N8N_AUDIO_WEBHOOK = "http://raspberrypi:5678/webhook/audio_trigger"

def audio_loop(person="Inconnu"):
    print("🎙️ Agent audio en écoute...")
    while True:
        try:
            wav_path = audio_manager.record_audio(duration=5)
            text = audio_manager.transcribe_audio(wav_path)
            if text and len(text.strip()) > 0:
                memory_manager.save_message(person, "user", text)
                requests.post(N8N_AUDIO_WEBHOOK, json={"person": person, "text": text}, timeout=10)
                print(f"📤 Message envoyé à n8n : {text}")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Erreur audio : {e}")
            time.sleep(5)

if __name__ == "__main__":
    audio_loop()
