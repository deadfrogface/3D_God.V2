import subprocess
import sys
import os
import datetime

def log(msg, level="INFO"):
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    prefix = {
        "INFO": "▶️",
        "SUCCESS": "✅",
        "ERROR": "❌"
    }.get(level, "▶️")
    print(f"[Launcher][main] {timestamp} {prefix} {msg}")

def main():
    log("Starte Launcher...", level="INFO")
    script = os.path.join(os.path.dirname(__file__), "main.py")

    if not os.path.isfile(script):
        log("main.py nicht gefunden! Stelle sicher, dass die Datei im selben Verzeichnis liegt.", level="ERROR")
        sys.exit(1)

    try:
        log(f"Führe {script} mit Python aus...", level="INFO")
        result = subprocess.run([sys.executable, script] + sys.argv[1:])
        log(f"main.py beendet mit Code {result.returncode}", level="SUCCESS" if result.returncode == 0 else "ERROR")
        sys.exit(result.returncode)
    except Exception as e:
        log(f"Ausnahme beim Ausführen von main.py: {e}", level="ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()