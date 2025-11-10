from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from scripts import vector_memory_manager as vec

router = APIRouter(prefix="/mcp/vector_memory", tags=["VectorMemory"])

class AddMemoryRequest(BaseModel):
    person: str
    text: str

class RecallRequest(BaseModel):
    person: str
    query: str
    n_results: int = 3

@router.post("/add")
async def add_memory(req: AddMemoryRequest):
    """Ajoute une mémoire sémantique pour une personne."""
    try:
        vec.add_memory(req.person, req.text)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recall")
async def recall(req: RecallRequest):
    """Recherche des souvenirs similaires à une requête."""
    try:
        results = vec.recall_memory(req.person, req.query, req.n_results)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
