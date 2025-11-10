from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, json

router = APIRouter(tags=["WebSocket"])
connected_clients = set()

@router.websocket("/mcp/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_clients.add(ws)
    print("🟢 Client WebSocket connecté")
    try:
        while True:
            msg = await ws.receive_text()
            data = json.loads(msg)
            await broadcast(data)
    except WebSocketDisconnect:
        connected_clients.remove(ws)
        print("🔴 Client déconnecté")

async def broadcast(message: dict):
    text = json.dumps(message)
    for ws in connected_clients.copy():
        try:
            await ws.send_text(text)
        except:
            connected_clients.remove(ws)