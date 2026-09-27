import sys
import os
import time
import socket
import webbrowser
import threading
import subprocess
import atexit

# Add studio directory to python path
STUDIO_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(STUDIO_DIR, ".."))
sys.path.insert(0, STUDIO_DIR)

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from app.server import app, socketio

PORT = int(os.environ.get("PORT", 5001))
LARAVEL_PORT = 8000
FRONTEND_URL = f"http://127.0.0.1:{LARAVEL_PORT}"

laravel_process = None

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def ensure_sqlite_db():
    db_path = os.path.join(PROJECT_ROOT, "database", "database.sqlite")
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with open(db_path, "w") as f:
            pass

def start_laravel():
    global laravel_process
    ensure_sqlite_db()
    if is_port_in_use(LARAVEL_PORT):
        print(f"[VisionCraft] Laravel server is already active on port {LARAVEL_PORT}.")
        return

    print(f"[VisionCraft] Starting Laravel Gateway (port {LARAVEL_PORT})...")
    try:
        laravel_process = subprocess.Popen(
            ["php", "artisan", "serve", f"--port={LARAVEL_PORT}"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        atexit.register(cleanup_laravel)
    except Exception as e:
        print(f"[VisionCraft] Warning: Could not start php artisan serve automatically: {e}")

def cleanup_laravel():
    global laravel_process
    if laravel_process and laravel_process.poll() is None:
        try:
            laravel_process.terminate()
        except Exception:
            pass

def open_browser():
    # Wait for Laravel to become responsive
    max_wait = 10
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if is_port_in_use(LARAVEL_PORT):
            break
        time.sleep(0.3)

    time.sleep(0.5)
    print(f"\n[VisionCraft] Opening Design Studio in browser: {FRONTEND_URL}\n")
    webbrowser.open(FRONTEND_URL)

if __name__ == "__main__":
    banner = f"""
    ========================================================================
             VISIONCRAFT - DIGITAL IMAGE PROCESSING STUDIO (DIP)
    ========================================================================
    * High-Performance Scientific Core: Pure Python, OpenCV, NumPy, SciPy
    * Backend Processing Microservice: http://127.0.0.1:{PORT}
    * Frontend Design Studio URL:     {FRONTEND_URL}
    ========================================================================
    """
    print(banner)

    # 1. Automatically start Laravel if not running
    start_laravel()

    # 2. Launch browser pointing to the Frontend Design Studio
    threading.Thread(target=open_browser, daemon=True).start()

    # 3. Start Python API Microservice
    socketio.run(app, host="127.0.0.1", port=PORT, debug=True, allow_unsafe_werkzeug=True)
