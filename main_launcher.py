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

IS_CODESPACE = os.environ.get("CODESPACES") == "true"


def install_codespace_dependencies():
    """
    Installs Qt/X11/Xvfb dependencies only if running inside GitHub Codespace.
    """
    log.info("🧪 Running in GitHub Codespace – installing system dependencies...")
    try:
        subprocess.check_call([
            "sudo", "apt-get", "update"
        ])
        subprocess.check_call([
            "sudo", "apt-get", "install", "-y",
            "xvfb", "libxcb1", "libxcb-util1", "libxcb-cursor0", "libxcb-keysyms1", "libxcb-xinerama0",
            "libxcb-randr0", "libxcb-shape0", "libxcb-icccm4", "libxcb-image0", "libxcb-xkb1",
            "libxkbcommon-x11-0", "libx11-xcb1", "libxrender1", "libxi6", "libxcomposite1",
            "libxcursor1", "libxrandr2", "libxtst6", "libegl1", "libgl1"
        ])
        log.success("✅ Qt/X11 dependencies installed (Codespace).")
    except Exception as e:
        log.error(f"❌ Failed to install system dependencies: {e}")
        log.debug(traceback.format_exc())


def ensure_fauxpilot_dependencies():
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
    try:
        import requests
        resp = requests.get(f"http://localhost:{FAUXPILOT_PORT}/", timeout=2)
        if resp.status_code == 200 and "FauxPilot" in resp.text:
            log.info(f"🧠 FauxPilot-Server already running and healthy on port {FAUXPILOT_PORT}.")
            return True
        else:
            log.warning(f"⚠️ FauxPilot-Server responded with status {resp.status_code}.")
    except Exception as e:
        log.debug(f"FauxPilot healthcheck failed: {e}")
    return False


def start_fauxpilot_server():
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


def setup_qt_offscreen_env():
    """
    Sets environment for Qt to run in headless/offscreen mode (only inside Codespaces).
    """
    try:
        import PySide6
        plugin_path = os.path.join(os.path.dirname(PySide6.__file__), "Qt", "plugins", "platforms")
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        log.info("🔧 Qt offscreen mode enabled (Codespace).")
    except Exception as e:
        log.warning(f"⚠️ Could not configure Qt offscreen mode: {e}")


def main():
    log.info("🧪 Starting 3D_God Launcher...")

    if IS_CODESPACE:
        install_codespace_dependencies()
        setup_qt_offscreen_env()
    else:
        log.info("🖥️ Running locally – using system display")

    try:
        ensure_fauxpilot_dependencies()
    except Exception as e:
        log.error(f"❌ Dependency check failed: {e}")
        log.debug(traceback.format_exc())
        return

    start_fauxpilot_server()

    script = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.isfile(script):
        log.error("main.py not found! Ensure the file is in the same directory.")
        return

    run_main_script(script)


def setup_signal_handlers():
    def cleanup(*args, **kwargs):
        stop_fauxpilot_server()
        sys.exit(0)
    atexit.register(stop_fauxpilot_server)
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)


if __name__ == "__main__":
    setup_signal_handlers()
    main()
    input("\n[🔚] Drücke Enter zum Beenden...")
