import subprocess
import time
import os
import signal

AGENTS = {
    "audio": "/app/agents/jetson_audio_agent.py",
    "camera": "/app/agents/jetson_camera_agent.py",
    "speaker": "/app/agents/jetson_speaker_agent.py",
    "system": "/app/agents/jetson_system_agent.py",
    "voice": "/app/agents/jetson_voice_command_agent.py"
}

PROCESSES = {}

def start_agent(name, path):
    print(f"🚀 Lancement de l’agent {name} ...")
    proc = subprocess.Popen(["python3", path])
    PROCESSES[name] = proc
    return proc

def stop_agent(name):
    proc = PROCESSES.get(name)
    if proc:
        proc.terminate()
        print(f"🛑 Agent {name} arrêté.")
        time.sleep(2)

def restart_agent(name):
    stop_agent(name)
    start_agent(name, AGENTS[name])

def monitor_loop():
    print("🧠 Superviseur d’agents actif.")
    for name, path in AGENTS.items():
        start_agent(name, path)

    try:
        while True:
            for name, proc in list(PROCESSES.items()):
                if proc.poll() is not None:  # Process mort
                    print(f"⚠️ Agent {name} s’est arrêté, redémarrage...")
                    start_agent(name, AGENTS[name])
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du superviseur.")
        for name in PROCESSES:
            stop_agent(name)

if __name__ == "__main__":
    monitor_loop()
