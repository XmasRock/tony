# ===============================
# Dockerfile : Tony AI Agents
# ===============================

# Image de base NVIDIA compatible Jetson (support GPU et PyTorch)
FROM nvcr.io/nvidia/l4t-pytorch:r35.3.1-pth2.0-py3

LABEL maintainer="Noel Jetson Project"
LABEL description="AI Agents stack for Jetson Orin Nano with LangChain, Ollama, Whisper, and n8n integration."

# --- Configuration système ---
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# --- Mises à jour et dépendances système ---
RUN apt-get update && apt-get install -y \
    git \
    portaudio19-dev \
    espeak \
    ffmpeg \
    libasound2-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --- Copier les fichiers du projet ---
COPY requirements.txt /app/requirements.txt
COPY agents /app/agents
COPY start_agents.py /app/start_agents.py

# --- Installer les dépendances Python ---
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# --- Exposer les ports ---
# 5050 = Command Server / 5051 = Speaker API / autres ports agents
EXPOSE 5050 5051 8000

# --- Commande par défaut ---
CMD ["python3", "start_agents.py"]
