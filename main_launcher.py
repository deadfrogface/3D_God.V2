import subprocess
import sys
import os
from core.logger import log

def main():
    log.info("Starte Launcher...")
    script = os.path.join(os.path.dirname(__file__), "main.py")

    if not os.path.isfile(script):
        log.error("main.py nicht gefunden! Stelle sicher, dass die Datei im selben Verzeichnis liegt.")
        sys.exit(1)

    try:
        log.info(f"Führe {script} mit Python aus...")
        result = subprocess.run([sys.executable, script] + sys.argv[1:])
        if result.returncode == 0:
            log.success(f"main.py beendet mit Code {result.returncode}")
        else:
            log.error(f"main.py beendet mit Code {result.returncode}")
        sys.exit(result.returncode)
    except Exception as e:
        log.error(f"Ausnahme beim Ausführen von main.py: {e}")
input("\n[🔚] Drücke Enter zum Beenden...")
if __name__ == "__main__":
    main()
