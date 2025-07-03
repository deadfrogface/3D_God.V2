import json
import subprocess
import os

class SculptTools:
    def __init__(self):
        print("[SculptBridge][__init__] ▶️ Initialisierung...")
        self.input_path = "blender_embed/sculpt_input.json"
        self.script_path = "blender_embed/sculpt_main.py"
        self.blender_path = self.get_blender_path()
        print("[SculptBridge][__init__] ✅ Pfade gesetzt")

    def get_blender_path(self):
        print("[SculptBridge][get_blender_path] ▶️ Lese Blender-Pfad aus config.json...")
        try:
            with open("config.json") as config_file:
                config = json.load(config_file)
                blender_path = config.get("blender_path", "blender.exe")
                print(f"[SculptBridge][get_blender_path] ✅ Blender-Pfad: {blender_path}")
                return blender_path
        except Exception as e:
            print(f"[SculptBridge][get_blender_path] ❌ Fehler beim Lesen der config.json: {e}")
            return "blender.exe"

    def send_data(self, sculpt_data):
        print(f"[SculptBridge][send_data] ▶️ Schreibe Sculpt-Daten nach {self.input_path}...")
        try:
            os.makedirs(os.path.dirname(self.input_path), exist_ok=True)
            with open(self.input_path, "w") as f:
                json.dump(sculpt_data, f, indent=4)
            print(f"[SculptBridge][send_data] ✅ Daten gespeichert")
        except Exception as e:
            print(f"[SculptBridge][send_data] ❌ Fehler beim Schreiben: {e}")

    def launch(self):
        print("[SculptBridge][launch] ▶️ Starte Blender-Prozess...")
        if not os.path.exists(self.blender_path):
            print(f"[SculptBridge][launch] ❌ Blender nicht gefunden unter {self.blender_path}")
            return

        abs_script_path = os.path.abspath(self.script_path)
        cmd = [
            self.blender_path,
            "--background",
            "--python", abs_script_path
        ]
        print(f"[SculptBridge][launch] ⚙️ Befehl: {' '.join(cmd)}")
        try:
            subprocess.Popen(cmd)
            print("[SculptBridge][launch] ✅ Blender-Launch ausgelöst")
        except Exception as e:
            print(f"[SculptBridge][launch] ❌ Fehler beim Starten von Blender: {e}")