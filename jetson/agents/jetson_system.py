# /jetson/agents/jetson_system.py

import time
import requests
import psutil
from scripts import system_manager, speaker_manager
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

N8N_SYSTEM_WEBHOOK = "http://raspberrypi:5678/webhook/system_status"

llm = Ollama(model="llama3", base_url="http://localhost:11434")

status_prompt = PromptTemplate.from_template("""
Voici les informations système actuelles du Jetson :
Température : {temp}°C
CPU : {cpu_usage}%
RAM : {ram_usage}%
Stockage : {disk_usage}%
Uptime : {uptime} heures

Résume ces données en une phrase concise, naturelle et positive à dire à voix haute.
""")

def system_monitor_loop():
    print("🧠 Agent système LangChain actif...")
    while True:
        try:
            # Récupération des infos système
            status = system_manager.get_system_status()
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            temp = status.get("temperature", 0)
            uptime = status.get("uptime", 0)

            # Génère un résumé avec Ollama
            summary = llm.invoke(status_prompt.format(
                temp=temp,
                cpu_usage=cpu,
                ram_usage=ram,
                disk_usage=disk,
                uptime=uptime
            ))

            print(f"📊 État : {summary}")

            # Envoi à n8n
            requests.post(N8N_SYSTEM_WEBHOOK, json={
                "temperature": temp,
                "cpu": cpu,
                "ram": ram,
                "disk": disk,
                "uptime": uptime,
                "summary": summary
            }, timeout=10)

            # Lecture à voix haute (facultatif)
            if cpu > 85 or temp > 75:
                warning = f"Attention, la charge du Jetson est élevée : {summary}"
                speaker_manager.say(warning)
            else:
                speaker_manager.say(summary)

            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Erreur agent système : {e}")
            time.sleep(30)

if __name__ == "__main__":
    system_monitor_loop()
