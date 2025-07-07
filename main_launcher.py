import subprocess
import sys
import os
import importlib
from core.logger import log

# 🧩 FauxPilot-Abhängigkeiten automatisch installieren
def ensure_fauxpilot_dependencies():
    packages = ["flask", "torch", "transformers", "requests"]
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            log.info(f"📦 Installiere fehlendes Paket: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 🧠 FauxPilot-Server starten (wenn nicht bereits läuft)
def start_fauxpilot_server():
    script_path = os.path.join(os.path.dirname(__file__), "ai_backend", "fauxpilot", "fauxpilot_server.py")

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

# 🚀 Hauptfunktion
def main():
    log.info("🧪 Starte 3D_God Launcher...")

    # Schritt 1: Abhängigkeiten prüfen
    try:
        ensure_fauxpilot_dependencies()
    except Exception as e:
        log.error(f"❌ Abhängigkeitsprüfung fehlgeschlagen: {e}")
        return

    # Schritt 2: FauxPilot starten
    start_fauxpilot_server()

    # Schritt 3: Main-Tool starten
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
