# runner.py
import subprocess
import sys
import time
import os
import signal
import asyncio

BACKEND_PATH = "src/main.py"
GUI_PATH = "src/gui.py"
COMPOSE_FILE = "docker-compose.yml"

def start_docker_compose():
    if os.path.exists(COMPOSE_FILE):
        print("Starting Docker Compose services...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    else:
        print("No docker-compose.yml file found")

def start_backend():
    print("Starting FastAPI backend...")
    backend_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app",
        "--reload",
        "--app-dir", "src"
    ])
    return backend_proc

def start_gui():
    print("Launching GUI...")
    gui_proc = subprocess.Popen([sys.executable, GUI_PATH])
    return gui_proc

def main():
    start_docker_compose()

    backend_proc = start_backend()
    time.sleep(2)
    gui_proc = start_gui()

    try:
        gui_proc.wait()
    finally:
        print("GUI closed, shutting down backend...")
        try:
            backend_proc.send_signal(signal.SIGINT)
            backend_proc.wait(timeout=5)
        except Exception:
            backend_proc.kill()
        print("All processes terminated.")

if __name__ == "__main__":
    main()
