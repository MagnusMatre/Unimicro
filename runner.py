# runner.py
import subprocess
import sys
import time
import os
import signal

BACKEND_PATH = "src/main.py"
GUI_PATH = "src/gui.py"
COMPOSE_FILE = "docker-compose.yml"

def check_docker():
    try:
        subprocess.run(["docker", "info"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Docker is running.")
    except subprocess.CalledProcessError:
        print("Docker is not running. Please start Docker Desktop manually.")
        sys.exit(1)

def start_docker_compose():
    if os.path.exists(COMPOSE_FILE):
        print("Starting Docker Compose services...")
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
    else:
        print("No docker-compose.yml file found. Skipping Docker Compose.")

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
    check_docker()
    start_docker_compose()

    backend_proc = start_backend()
    # Give backend a moment to start
    time.sleep(2)
    gui_proc = start_gui()

    try:
        # Wait for GUI to exit
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
