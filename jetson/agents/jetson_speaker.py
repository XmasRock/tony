from scripts import speaker_manager
import requests
import time

N8N_SPEAKER_WEBHOOK = "http://raspberrypi:5678/webhook/speaker_output"

def speaker_loop():
    print("🔊 Agent haut-parleur en attente de messages...")
    while True:
        try:
            # Option : vérifier s'il y a un message en attente depuis n8n
            resp = requests.get(N8N_SPEAKER_WEBHOOK, timeout=5)
            if resp.status_code == 200:
                text = resp.json().get("text")
                if text:
                    speaker_manager.say(text)
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Erreur speaker : {e}")
            time.sleep(10)

if __name__ == "__main__":
    speaker_loop()
