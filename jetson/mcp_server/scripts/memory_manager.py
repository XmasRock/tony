import os
import json
from datetime import datetime
from typing import Optional, Dict, List

DATA_DIR = "/app/data/conversations"

os.makedirs(DATA_DIR, exist_ok=True)


def _get_file_path(person: str) -> str:
    """Retourne le chemin du fichier JSON associé à une personne."""
    safe_name = person.replace(" ", "_").lower()
    return os.path.join(DATA_DIR, f"{safe_name}.json")


def get_conversation(person: str) -> Optional[Dict]:
    """Charge la conversation d’une personne depuis le stockage JSON."""
    path = _get_file_path(person)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_message(person: str, sender: str, text: str) -> None:
    """Ajoute un message à la conversation d’une personne."""
    conv = get_conversation(person) or {"person": person, "messages": []}
