import subprocess
import json
import os

class SculptTools:
    def __init__(self):
        self.blender_path = "blender"  # ggf. absoluter Pfad
        self.script_path = "blender_embed/scripts/sculpt_apply.py"
        self.data_path = "blender_embed/sculpt_input.json"

    def launch(self):
        print("[Sculpt] Starte Blender-Sculpt-Modus...")
        subprocess.Popen([
            self.blender_path,
            "--python", self.script_path
        ])

    def run_script(self, script_name):
        print(f"[BlenderBridge] Starte Blender-Skript: {script_name}")
        subprocess.call([
            self.blender_path,
            "--background",
            "--python", f"blender_embed/scripts/{script_name}"
        ])

    def send_data(self, sculpt_data):
        with open(self.data_path, "w") as f:
            json.dump(sculpt_data, f, indent=4)
        print(f"[Sculpt] Daten geschrieben → {self.data_path}")