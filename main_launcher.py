import subprocess
import sys
import os
from core.logger import log

def start_fauxpilot_server():
    """Startet FauxPilot-Server, falls er nicht bereits läuft."""
    script_path = os.path.join(os.path.dirname(__file__), "ai_backend", "fauxpilot", "fauxpilot_server.py")

    # Prüfe, ob der Server schon läuft
    try:
        import requests
        requests.get("http://localhost:5000", timeout=1)
        log.info("🧠 FauxPilot-Server läuft bereits.")
        return
    except:
        log.info("⚡ Starte FauxPilot-Server im Hintergrund...")

    try:
        subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        log.success("✅ FauxPilot-Server gestartet.")
    except Exception as e:
        log.error(f"❌ Fehler beim Start von FauxPilot-Server: {e}")

def main():
    log.info("🧪 Starte 3D_God Launcher...")

    # Starte FauxPilot zuerst
    start_fauxpilot_server()

    # Starte dein eigentliches Tool
    script = os.path.join(os.path.dirname(__file__), "main.py")

    if not os.path.isfile(script):
        log.error("main.py nicht gefunden! Stelle sicher, dass die Datei im selben Verzeichnis liegt.")
        return

    try:
        log.info(f"▶️ Führe {script} mit Python aus...")
        result = subprocess.run([sys.executable, script] + sys.argv[1:])
        if result.returncode == 0:
            log.success(f"main.py beendet mit Code {result.returncode}")
        else:
            log.error(f"main.py beendet mit Code {result.returncode}")
    except Exception as e:
        log.error(f"❌ Ausnahme beim Ausführen von main.py: {e}")

if __name__ == "__main__":
    main()
    input("\n[🔚] Drücke Enter zum Beenden...")
