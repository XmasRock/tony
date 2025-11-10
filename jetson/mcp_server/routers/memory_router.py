from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from scripts import memory_manager as mem

router = APIRouter(prefix="/mcp/memory", tags=["Memory"])

class Message(BaseModel):
    sender: str
    text: str

class SaveRequest(BaseModel):
    person: str
    message: Message

class PersonRequest(BaseModel):
    person: str

@router.post("/save")
async def save_message(req: SaveRequest):
    """Ajoute un message à la conversation."""
    try:
        mem.save_message(req.person, req.message.sender, req.message.text)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get")
async def get_conversation(req: PersonRequest):
    """Retourne la conversation complète d’une personne."""
    conv = mem.get_conversation(req.person)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation introuvable.")
    return conv

@router.post("/summary")
async def summarize(req: PersonRequest):
    """Retourne un résumé des derniers messages."""
    return {"summary": mem.summarize_conversation(req.person)}

@router.get("/people")
async def list_people():
    """Liste toutes les personnes connues."""
    return {"people": mem.list_known_people()}
