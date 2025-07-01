import json
import os
import subprocess

class SculptTools:
    def __init__(self):
        self.input_path = "blender_embed/sculpt_input.json"
        self.script_path = "blender_embed/sculpt_main.py"
        self.blender_path = "blender_embed/blender.exe"  # ⬅ Optional: anpassbar

    def send_data(self, sculpt_data):
        with open(self.input_path, "w") as f:
            json.dump(sculpt_data, f, indent=4)
        print(f"[SculptBridge] Daten geschrieben → {self.input_path}")

    def launch(self):
        if not os.path.exists(self.blender_path):
            print("[SculptBridge] Fehler: Blender.exe nicht gefunden!")
            return

        cmd = [
            self.blender_path,
            "--background",
            "--python", self.script_path
        ]
        print(f"[SculptBridge] Starte Blender-Script...\n{' '.join(cmd)}")
        subprocess.Popen(cmd)