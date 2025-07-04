import json
import subprocess
from pathlib import Path
from core.logger import log

class BlenderBridge:
    def __init__(self, config_path="config.json"):
        log.info("[BlenderBridge][__init__] ▶️ Initialisierung...")
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        log.info(f"[BlenderBridge][load_config] ▶️ Lade Konfiguration aus: {self.config_path}")
        path = Path(self.config_path)
        if not path.exists():
            log.error(f"[BlenderBridge][load_config] ❌ Datei nicht gefunden: {self.config_path}")
            raise FileNotFoundError(f"Konfiguration fehlt: {self.config_path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            self.blender_path = self.config.get("blender_path", "")
            log.success(f"[BlenderBridge][load_config] ✅ Konfiguration geladen. Blender-Pfad: {self.blender_path}")
        except Exception as e:
            log.error(f"[BlenderBridge][load_config] ❌ Fehler beim Laden der Config: {e}")
            raise

    def run_blender_script(self, script_name, args=None):
        log.info(f"[BlenderBridge][run_blender_script] ▶️ Starte Skript: {script_name}")
        args = args or []
        script_path = f"blender_embedded/scripts/{script_name}"

        if not Path(script_path).exists():
            log.error(f"[BlenderBridge][run_blender_script] ❌ Blender-Skript nicht gefunden: {script_path}")
            return False

        cmd = [
            self.blender_path,
            "--background",
            "--python", script_path,
            "--"
        ] + args

        log.debug(f"[BlenderBridge][run_blender_script] ⚙️ Kommando: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            log.success("[BlenderBridge][run_blender_script] ✅ Skript erfolgreich ausgeführt")
            return True
        except subprocess.CalledProcessError as e:
            log.error(f"[BlenderBridge][run_blender_script] ❌ Fehler beim Ausführen: {e}")
            return False