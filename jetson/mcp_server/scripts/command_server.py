# /jetson/mcp_server/scripts/command_server.py

from fastapi import FastAPI, Request
import subprocess
import os
import signal
from jetson.agents import jetson_master_agent

app = FastAPI(title="Jetson Command Server")

@app.post("/command")
async def receive_command(request: Request):
    data = await request.json()
    command = data.get("command")
    target = data.get("target")

    if command == "restart_agent" and target:
        restarted = restart_agent(target)
        return {"status": "ok", "message": f"Agent {target} redémarré : {restarted}"}

    elif command == "shutdown":
        os.system("sudo shutdown now")
        return {"status": "ok", "message": "Arrêt du Jetson en cours"}

    elif command == "reboot":
        os.system("sudo reboot")
        return {"status": "ok", "message": "Reboot du Jetson en cours"}

    else:
        return {"status": "error", "message": f"Commande inconnue : {command}"}

def restart_agent(agent_name: str):
    try:
        for proc in jetson_master_agent.AGENT_PROCESSES.values():
            if agent_name in str(proc.args):
                os.kill(proc.pid, signal.SIGTERM)
                print(f"🌀 Redémarrage agent {agent_name}...")
        jetson_master_agent.start_agent(agent_name, jetson_master_agent.AGENTS[agent_name])
        return True
    except Exception as e:
        print(f"⚠️ Erreur redémarrage {agent_name}: {e}")
        return False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
