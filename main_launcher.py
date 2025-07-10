import subprocess
import sys
import os
import importlib
import signal
import atexit
import traceback
from core.logger import log

FAUXPILOT_PORT = int(os.environ.get("FAUXPILOT_PORT", 5000))
FAUXPILOT_PROCESS = None

def ensure_fauxpilot_dependencies():
    """
    Ensures required dependencies for FauxPilot are installed.
    Uses requirements.txt if present, otherwise checks individual packages.
    """
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.isfile(requirements_file):
        log.info("📦 Installing dependencies from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            log.success("✅ requirements.txt dependencies installed.")
            return
        except Exception as e:
            log.error(f"❌ Failed to install requirements.txt dependencies: {e}")
            log.debug(traceback.format_exc())

    packages = ["flask", "torch", "transformers", "requests"]
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError as e:
            log.info(f"📦 Installing missing package: {package}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception as inst_e:
                log.error(f"❌ Failed to install package {package}: {inst_e}")
                log.debug(traceback.format_exc())

def fauxpilot_server_healthcheck():
    """
    Checks if FauxPilot server is running and healthy.
    Returns True if server responds with expected status, else False.
    """
    try:
        import requests
        resp = requests.get(f"http://localhost:{FAUXPILOT_PORT}/", timeout=2)
        if resp.status_code == 200 and "FauxPilot" in resp.text:  # Replace with a specific check if you have an endpoint
            log.info(f"🧠 FauxPilot-Server already running and healthy on port {FAUXPILOT_PORT}.")
            return True
        else:
            log.warning(f"⚠️ FauxPilot-Server responded with status {resp.status_code}.")
    except Exception as e:
        log.debug(f"FauxPilot healthcheck failed: {e}")
    return False

def start_fauxpilot_server():
    """
    Starts the FauxPilot server in the background if not already running.
    """
    global FAUXPILOT_PROCESS
    script_path = os.path.join(os.path.dirname(__file__), "ai_backend", "fauxpilot", "fauxpilot_server.py")
    if fauxpilot_server_healthcheck():
        return

    log.info(f"⚡ Starting FauxPilot-Server in background on port {FAUXPILOT_PORT}...")
    try:
        FAUXPILOT_PROCESS = subprocess.Popen(
            [sys.executable, script_path, "--port", str(FAUXPILOT_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log.success("✅ FauxPilot-Server started.")
    except Exception as e:
        log.error(f"❌ Error starting FauxPilot-Server: {e}")
        log.debug(traceback.format_exc())

def stop_fauxpilot_server():
    """
    Gracefully stops the FauxPilot server if it was started by this launcher.
    """
    global FAUXPILOT_PROCESS
    if FAUXPILOT_PROCESS and FAUXPILOT_PROCESS.poll() is None:
        log.info("🛑 Stopping FauxPilot-Server...")
        try:
            FAUXPILOT_PROCESS.terminate()
            FAUXPILOT_PROCESS.wait(timeout=5)
            log.success("✅ FauxPilot-Server stopped.")
        except Exception as e:
            log.error(f"❌ Error stopping FauxPilot-Server: {e}")
            log.debug(traceback.format_exc())

def run_main_script(script):
    """
    Runs the given script with the current python executable and passes command line args.
    """
    try:
        log.info(f"▶️ Running {script} with Python...")
        result = subprocess.run([sys.executable, script] + sys.argv[1:])
        if result.returncode == 0:
            log.success(f"{os.path.basename(script)} exited with code {result.returncode}")
        else:
            log.error(f"{os.path.basename(script)} exited with code {result.returncode}")
    except Exception as e:
        log.error(f"❌ Exception while running {os.path.basename(script)}: {e}")
        log.debug(traceback.format_exc())

def main():
    """
    Main entry point for the launcher.
    """
    log.info("🧪 Starting 3D_God Launcher...")

    # Step 1: Check dependencies
    try:
        ensure_fauxpilot_dependencies()
    except Exception as e:
        log.error(f"❌ Dependency check failed: {e}")
        log.debug(traceback.format_exc())
        return

    # Step 2: Start FauxPilot
    start_fauxpilot_server()

    # Step 3: Run main tool
    script = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.isfile(script):
        log.error("main.py not found! Ensure the file is in the same directory.")
        return

    run_main_script(script)

def setup_signal_handlers():
    """
    Set up signal and exit handlers for graceful termination.
    """
    def cleanup(*args, **kwargs):
        stop_fauxpilot_server()
        sys.exit(0)
    atexit.register(stop_fauxpilot_server)
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    setup_signal_handlers()
    main()
    input("\n[🔚] Drücke Enter zum Beenden...")  # Kept as per your request (improvement #11 excluded)
