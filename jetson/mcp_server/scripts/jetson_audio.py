import speech_recognition as sr
import asyncio
import websockets
import json
import os

SERVER_WS = os.getenv("SERVER_WS", "ws://localhost:8000/mcp/ws")

async def send_event(event_type, payload):
    async with websockets.connect(SERVER_WS) as ws:
        await ws.send(json.dumps({"type": event_type, "payload": payload}))

async def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("🎙️  Écoute du micro Jetson en cours...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print("Parlez...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="fr-FR")
                print(f"🗣️ Vous avez dit : {text}")
                await send_event("audio.transcription", {"text": text})
            except sr.UnknownValueError:
                print("🤔 Non compris.")
            except sr.RequestError as e:
                print(f"⚠️ Erreur API : {e}")

if __name__ == "__main__":
    asyncio.run(main())
