import json
import os
import subprocess

class SculptTools:
    def __init__(self):
        print("[SculptTool][__init__] ▶️ Initialisierung gestartet...")
        self.input_path = "blender_embed/sculpt_input.json"
        self.script_path = "blender_embed/sculpt_main.py"
        self.blender_path = "blender_embed/blender.exe"  # ⬅ Optional: anpassbar
        print(f"[SculptTool][__init__] ✅ Pfade gesetzt:\n - input: {self.input_path}\n - script: {self.script_path}\n - blender: {self.blender_path}")

    def send_data(self, sculpt_data):
        print("[SculptTool][send_data] ▶️ Speichere Sculpt-Daten...")
        try:
            with open(self.input_path, "w") as f:
                json.dump(sculpt_data, f, indent=4)
            print(f"[SculptTool][send_data] ✅ Daten erfolgreich geschrieben nach: {self.input_path}")
        except Exception as e:
            print(f"[SculptTool][send_data] ❌ Fehler beim Schreiben der Datei: {e}")

    def launch(self):
        print("[SculptTool][launch] ▶️ Starte Blender-Script...")

        if not os.path.exists(self.blender_path):
            print(f"[SculptTool][launch] ❌ Fehler: Blender.exe nicht gefunden unter: {self.blender_path}")
            return

        cmd = [
            self.blender_path,
            "--background",
            "--python", self.script_path
        ]

        try:
            print(f"[SculptTool][launch] ⚙️ Befehl: {' '.join(cmd)}")
            subprocess.Popen(cmd)
            print("[SculptTool][launch] ✅ Blender wurde im Hintergrund gestartet.")
        except Exception as e:
            print(f"[SculptTool][launch] ❌ Fehler beim Starten von Blender: {e}")