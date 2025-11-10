import asyncio
import websockets
import json
import os

SERVER_WS = os.getenv("SERVER_WS", "ws://<IP_JETSON>:8000/mcp/ws")

async def main():
    async with websockets.connect(SERVER_WS) as ws:
        print("📸 Connecté au Jetson MCP pour caméra")
        async for msg in ws:
            data = json.loads(msg)
            if data.get("type") == "camera.person_detected":
                print(f"👤 Détection : {data['payload']['person']}")

if __name__ == "__main__":
    asyncio.run(main())
