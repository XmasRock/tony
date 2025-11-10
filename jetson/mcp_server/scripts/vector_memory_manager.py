import chromadb
from chromadb.config import Settings
import requests
import os
import json
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = os.getenv("EMBED_MODEL", "mxbai-embed-large")
CHROMA_PATH = "/app/data/embeddings"

os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection("jetson_memory")

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Demande à Ollama de créer les embeddings d’une liste de textes."""
    embeddings = []
    for text in texts:
        payload = {"model": EMBED_MODEL, "prompt": text}
        r = requests.post(OLLAMA_URL, json=payload)
        if r.status_code == 200:
            data = r.json()
            embeddings.append(data["embedding"])
        else:
            print(f"⚠️ Erreur embedding Ollama: {r.text}")
    return embeddings


def add_memory(person: str, text: str):
    """Ajoute un souvenir sémantique pour une personne."""
    embedding = embed_texts([text])[0]
    collection.add(
        ids=[f"{person}-{len(collection.get()['ids'])+1}"],
        embeddings=[embedding],
        metadatas=[{"person": person}],
        documents=[text]
    )
    print(f"🧠 Souvenir ajouté pour {person}")


def recall_memory(person: str, query: str, n_results: int = 3) -> List[Dict]:
    """Recherche les souvenirs les plus similaires à la requête."""
    embedding = embed_texts([query])[0]
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={"person": person}
    )
    memories = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        memories.append({"person": meta["person"], "text": doc})
    return memories


if __name__ == "__main__":
    add_memory("Valérie", "Nous avons parlé de son entraînement en roller.")
    add_memory("Valérie", "Elle travaille maintenant comme auxiliaire de vie.")
    recal
