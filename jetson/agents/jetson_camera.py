from scripts import camera_manager, memory_manager
import requests
import time

N8N_CAMERA_WEBHOOK = "http://raspberrypi:5678/webhook/camera_trigger"

def camera_loop():
    print("📸 Agent caméra en écoute...")
    while True:
        try:
            person = camera_manager.recognize_person()
            if person:
                summary = memory_manager.summarize_conversation(person)
                payload = {"person": person, "summary": summary}
                requests.post(N8N_CAMERA_WEBHOOK, json=payload, timeout=10)
                print(f"✅ {person} reconnu, conversation relancée.")
                time.sleep(10)
            else:
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ Erreur caméra : {e}")
            time.sleep(5)

if __name__ == "__main__":
    camera_loop()
