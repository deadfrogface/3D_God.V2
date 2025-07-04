import json
import os
import subprocess
from core.logger import log

class SculptTools:
    def __init__(self):
        log.info("[SculptTool][__init__] ▶️ Initialisierung gestartet...")
        self.input_path = "blender_embed/sculpt_input.json"
        self.script_path = "blender_embed/sculpt_main.py"
        self.blender_path = "blender_embed/blender.exe"  # ⬅ Optional: anpassbar
        log.success(f"[SculptTool][__init__] ✅ Pfade gesetzt:\n - input: {self.input_path}\n - script: {self.script_path}\n - blender: {self.blender_path}")

    def send_data(self, sculpt_data):
        log.info("[SculptTool][send_data] ▶️ Speichere Sculpt-Daten...")
        try:
            with open(self.input_path, "w") as f:
                json.dump(sculpt_data, f, indent=4)
            log.success(f"[SculptTool][send_data] ✅ Daten erfolgreich geschrieben nach: {self.input_path}")
        except Exception as e:
            log.error(f"[SculptTool][send_data] ❌ Fehler beim Schreiben der Datei: {e}")

    def launch(self):
        log.info("[SculptTool][launch] ▶️ Starte Blender-Script...")

        if not os.path.exists(self.blender_path):
            log.error(f"[SculptTool][launch] ❌ Fehler: Blender.exe nicht gefunden unter: {self.blender_path}")
            return

        cmd = [
            self.blender_path,
            "--background",
            "--python", self.script_path
        ]

        try:
            log.debug(f"[SculptTool][launch] ⚙️ Befehl: {' '.join(cmd)}")
            subprocess.Popen(cmd)
            log.success("[SculptTool][launch] ✅ Blender wurde im Hintergrund gestartet.")
        except Exception as e:
            log.error(f"[SculptTool][launch] ❌ Fehler beim Starten von Blender: {e}")