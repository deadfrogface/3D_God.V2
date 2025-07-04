import json
import subprocess
import os
from core.logger import log

class SculptTools:
    def __init__(self):
        log.info("[SculptBridge][__init__] ▶️ Initialisierung...")
        self.input_path = "blender_embed/sculpt_input.json"
        self.script_path = "blender_embed/sculpt_main.py"
        self.blender_path = self.get_blender_path()
        log.success("[SculptBridge][__init__] ✅ Pfade gesetzt")

    def get_blender_path(self):
        log.info("[SculptBridge][get_blender_path] ▶️ Lese Blender-Pfad aus config.json...")
        try:
            with open("config.json") as config_file:
                config = json.load(config_file)
                blender_path = config.get("blender_path", "blender.exe")
                log.success(f"[SculptBridge][get_blender_path] ✅ Blender-Pfad: {blender_path}")
                return blender_path
        except Exception as e:
            log.error(f"[SculptBridge][get_blender_path] ❌ Fehler beim Lesen der config.json: {e}")
            return "blender.exe"

    def send_data(self, sculpt_data):
        log.info(f"[SculptBridge][send_data] ▶️ Schreibe Sculpt-Daten nach {self.input_path}...")
        try:
            os.makedirs(os.path.dirname(self.input_path), exist_ok=True)
            with open(self.input_path, "w") as f:
                json.dump(sculpt_data, f, indent=4)
            log.success(f"[SculptBridge][send_data] ✅ Daten gespeichert")
        except Exception as e:
            log.error(f"[SculptBridge][send_data] ❌ Fehler beim Schreiben: {e}")

    def launch(self):
        log.info("[SculptBridge][launch] ▶️ Starte Blender-Prozess...")
        if not os.path.exists(self.blender_path):
            log.error(f"[SculptBridge][launch] ❌ Blender nicht gefunden unter {self.blender_path}")
            return

        abs_script_path = os.path.abspath(self.script_path)
        cmd = [
            self.blender_path,
            "--background",
            "--python", abs_script_path
        ]
        log.debug(f"[SculptBridge][launch] ⚙️ Befehl: {' '.join(cmd)}")
        try:
            subprocess.Popen(cmd)
            log.success("[SculptBridge][launch] ✅ Blender-Launch ausgelöst")
        except Exception as e:
            log.error(f"[SculptBridge][launch] ❌ Fehler beim Starten von Blender: {e}")