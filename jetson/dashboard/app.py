# /jetson/dashboard/app.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import psutil
import json
import datetime

LOG_DIR = Path("/var/log/tony_agents")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

app = FastAPI(title="Tony IA Dashboard")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # État des processus
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if "jetson_" in proc.info['name']:
            processes.append(proc.info)

    # Logs récents
    logs = {}
    for log_file in LOG_DIR.glob("*.log"):
        with open(log_file) as f:
            lines = f.readlines()[-5:]
        logs[log_file.stem] = lines

    # Infos système
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = datetime.timedelta(seconds=int(psutil.boot_time()))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "processes": processes,
        "logs": logs,
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "uptime": uptime
    })
