# tony
My J.A.R.V.I.S is called Tony

# 🧠 Jetson AI Agent Framework

Architecture IA locale basée sur **Jetson Orin Nano + Raspberry Pi + Ollama + n8n**,  
permettant des interactions vocales et visuelles entièrement locales, sans cloud.

---

## 🚀 Objectif

Créer un agent IA **autonome et contextuel** capable de :
- détecter et reconnaître une personne via la caméra 🎥  
- écouter et comprendre via le micro 🎤  
- répondre vocalement via le haut-parleur 🔊  
- conserver une mémoire à court et long terme 🧠  
- orchestrer les flux via n8n ⚙️

---

## 🏗️ Architecture

[ Caméra | Micro | Speaker ]
↓
[ Jetson Orin Nano ]

Ollama (LLM local)

MCP Server (FastAPI)

Mémoire (JSON + Vector)

Agents (caméra, audio, système)
↓
[ Raspberry Pi ]

n8n orchestrateur

Workflows (IA, triggers)
↓
[ PC Windows ]

Interface n8n (via navigateur)

# Lancer le serveur
```
uvicorn main:app --host 0.0.0.0 --port 8000
```


# Lancer les agents

Dans des terminaux séparés :
```
python3 agents/jetson_camera.py
python3 agents/jetson_audio.py
python3 agents/jetson_speaker.py
python3 agents/jetson_system.py
```

# Intégration n8n (Raspberry Pi)

Lancer n8n : n8n start --tunnel

Créer les webhooks suivants :

/webhook/camera_trigger

/webhook/audio_trigger

/webhook/speaker_output

/webhook/system_status

Chaque webhook déclenche un workflow IA utilisant :

un nœud HTTP → Jetson MCP (/mcp/memory + /mcp/vector_memory)

un nœud Ollama → modèle IA local

un nœud HTTP → Jetson speaker (pour parler)

# Stockage
|Type	| Emplacement |	Format |
|Conversations|	/app/data/conversations|	JSON|
|Mémoire vectorielle|	/app/data/embeddings|	ChromaDB|
|Audio / Images	|/app/data/audio / /app/data/camera|	WAV / JPG|
|Config	|/app/config/|	Texte / JSON|

# Prompt IA de base
```
Tu es l’assistant personnel de Valérie.
Tu discutes naturellement, en gardant le contexte de ses précédentes conversations.
Sois bienveillant, précis, et capable d’évoquer ses souvenirs (travail, sport, etc.).
Si Valérie revient, salue-la en résumant brièvement votre dernière discussion.
```

# Notes techniques

Compatible Jetson Orin Nano, Ubuntu 22.04, Python 3.10+
Ollama doit tourner sur le Jetson (ou en réseau local sur un PC puissant).
Le Raspberry Pi héberge n8n et le relie aux autres agents.
Le SSD 2 To sert de stockage conversationnel et vectoriel.

# Licence
MIT — libre à usage personnel ou expérimental.