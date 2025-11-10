import psutil
import subprocess
import os

def get_system_status():
    """Retourne les informations système principales du Jetson."""
    cpu_usage = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    gpu_temp = None
    try:
        output = subprocess.check_output(
            ["cat", "/sys/devices/gpu.0/temp"],
            text=True
        )
        gpu_temp = int(output) / 1000
    except Exception:
        pass

    return {
        "cpu_usage": f"{cpu_usage:.1f}%",
        "memory": f"{mem.percent:.1f}%",
        "disk_usage": f"{disk.percent:.1f}%",
        "gpu_temp": f"{gpu_temp}°C" if gpu_temp else "N/A",
        "uptime": f"{psutil.boot_time():.0f}"
    }

if __name__ == "__main__":
    print(get_system_status())
