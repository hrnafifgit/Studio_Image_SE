import sys
import os
import time
import webbrowser
import threading

# Add studio directory to python path
STUDIO_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, STUDIO_DIR)

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from app.server import app, socketio

PORT = int(os.environ.get("PORT", 5001))

def open_browser():
    time.sleep(1.2)
    url = f"http://127.0.0.1:{PORT}"
    print(f"\n[VisionCraft] Opening DIP Photoshop Studio in browser: {url}\n")
    webbrowser.open(url)

if __name__ == "__main__":
    banner = f"""
    ========================================================================
             VISIONCRAFT - DIGITAL IMAGE PROCESSING STUDIO (DIP)
    ========================================================================
    * High-Performance Scientific Core: Pure Python, OpenCV, NumPy, SciPy
    * Web Photoshop DIP Studio Running at: http://127.0.0.1:{PORT}
    * Operations: Point Ops, Spatial Filters, Frequency (FFT), Morphology,
                  Edge Detection, Color Spaces & Image Restoration
    ========================================================================
    """
    print(banner)
    threading.Thread(target=open_browser, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=PORT, debug=True, allow_unsafe_werkzeug=True)
