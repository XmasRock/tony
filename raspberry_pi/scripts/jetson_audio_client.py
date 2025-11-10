import asyncio
import websockets
import json
import pyttsx3
import os

SERVER_WS = os.getenv("SERVER_WS", "ws://<IP_JETSON>:8000/mcp/ws")

engine = pyttsx3.init()

async def main():
    async with websockets.connect(SERVER_WS) as ws:
        print("🔊 Connecté au serveur Jetson MCP")
        async for message in ws:
            data = json.loads(message)
            if data.get("type") == "tts.speak":
                text = data["payload"].get("text", "")
                print(f"💬 Lecture : {text}")
                engine.say(text)
                engine.runAndWait()

if __name__ == "__main__":
    asyncio.run(main())
