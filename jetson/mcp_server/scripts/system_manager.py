# /jetson/mcp_server/scripts/system_manager.py

import psutil
import time

def get_temperature():
    """Récupère la température CPU du Jetson."""
    try:
        with open("/sys/devices/virtual/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read().strip()) / 1000
    except Exception:
        return 0.0

def get_system_status():
    """Retourne un dictionnaire complet d’état système."""
    temp = get_temperature()
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    uptime = time.time() - psutil.boot_time()

    return {
        "temperature": temp,
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "uptime": round(uptime / 3600, 2)  # en heures
    }
