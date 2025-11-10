# /jetson/agents/jetson_master_agent.py

import os
import time
import subprocess
import psutil
from pathlib import Path

AGENTS = {
    "camera": "jetson_camera.py",
    "audio": "jetson_audio.py",
    "speaker": "jetson_speaker.py",
    "system": "jetson_system.py"
}

LOG_DIR = Path("/var/log/jetson_agents")
LOG_DIR.mkdir(parents=True, exist_ok=True)

AGENT_PROCESSES = {}

def start_agent(name, script):
    log_file = LOG_DIR / f"{name}.log"
    process = subprocess.Popen(
        ["python3", str(Path(__file__).parent / script)],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT
    )
    AGENT_PROCESSES[name] = process
    print(f"✅ Agent {name} lancé (PID={process.pid})")

def monitor_agents():
    for name, process in list(AGENT_PROCESSES.items()):
        if process.poll() is not None:
            print(f"⚠️ Agent {name} a cessé de fonctionner. Redémarrage...")
            start_agent(name, AGENTS[name])

def kill_all_agents():
    for name, process in AGENT_PROCESSES.items():
        process.terminate()
    AGENT_PROCESSES.clear()
    print("🛑 Tous les agents ont été arrêtés proprement.")

def master_loop():
    print("🧠 Agent de coordination Jetson actif...")
    # Lancer tous les agents au démarrage
    for name, script in AGENTS.items():
        start_agent(name, script)

    try:
        while True:
            monitor_agents()
            time.sleep(10)
    except KeyboardInterrupt:
        kill_all_agents()

if __name__ == "__main__":
    master_loop()
