from fastapi import FastAPI
from jetson.mcp_server.routers.memory_router import router as memory_router
from jetson.mcp_server.routers.vector_memory_router import router as vector_memory_router
from jetson.mcp_server.routers.ws_router import router as ws_router
from jetson.mcp_server.routers.tts_router import router as tts_router
from jetson.mcp_server.routers.camera_router import router as camera_router

app = FastAPI(title="Jetson MCP Server")

# Inclure tous les routers
app.include_router(memory_router)
app.include_router(vector_memory_router)
app.include_router(ws_router)
app.include_router(tts_router)
app.include_router(camera_router)


@app.get("/")
def home():
    return {"status": "Jetson MCP online", "modules": ["camera", "audio", "memory", "vector_memory"]}