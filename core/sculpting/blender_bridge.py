import json
import subprocess
from pathlib import Path

class BlenderBridge:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        path = Path(self.config_path)
        if not path.exists():
            raise FileNotFoundError(f"Konfiguration fehlt: {self.config_path}")
        with open(path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.blender_path = self.config.get("blender_path", "")

    def run_blender_script(self, script_name, args=None):
        args = args or []
        script_path = f"blender_embedded/scripts/{script_name}"
        if not Path(script_path).exists():
            print(f"❌ Blender-Skript nicht gefunden: {script_path}")
            return False

        cmd = [
            self.blender_path,
            "--background",
            "--python", script_path,
            "--"
        ] + args

        print(f"🎮 Starte Blender mit: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print("✅ Blender-Skript ausgeführt")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Blender-Fehler: {e}")
            return False
