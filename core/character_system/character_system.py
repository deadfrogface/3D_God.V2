import os
import json
from core.sculpting.sculpt_bridge import SculptTools

class CharacterSystem:
    def __init__(self):
        self.config_path = "config.json"
        self.preset_path = "presets/"
        self.sculpt_data = {
            "height": 50,
            "breast_size": 50,
            "hip_width": 50,
            "arm_length": 50,
            "leg_length": 50
        }
        self.anatomy_state = {
            "skin": True,
            "fat": True,
            "muscle": False,
            "bone": False,
            "organs": False
        }
        self.config = self.load_config()
        self.sculpt_tools = SculptTools()
        self.nsfw_enabled = self.config.get("nsfw_enabled", True)

    def load_config(self):
        if not os.path.exists(self.config_path):
            return {"theme": "dark", "nsfw_enabled": True, "controller_enabled": True}
        with open(self.config_path, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def update_sculpt_value(self, key, value):
        self.sculpt_data[key] = value
        print(f"[Sculpt] {key}: {value}")
        # Optional: hier Viewport oder Blender live ansprechen

    def sculpt(self):
        print("[Sculpt] Blender Sculpting wird gestartet...")
        self.sculpt_tools.launch()

    def run_blender_script(self, script_name):
        print(f"[Sculpt] Führe Blender-Skript aus: {script_name}")
        self.sculpt_tools.run_script(script_name)

    def save_preset(self, name="default"):
        if not os.path.exists(self.preset_path):
            os.makedirs(self.preset_path)
        path = os.path.join(self.preset_path, f"{name}.json")
        with open(path, "w") as f:
            json.dump({
                "sculpt_data": self.sculpt_data,
                "nsfw": self.nsfw_enabled,
                "anatomy": self.anatomy_state
            }, f, indent=4)
        print(f"[Preset] Gespeichert: {path}")

    def load_preset(self, name="default"):
        path = os.path.join(self.preset_path, f"{name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.sculpt_data = data.get("sculpt_data", {})
                self.nsfw_enabled = data.get("nsfw", True)
                self.anatomy_state = data.get("anatomy", {})
            self.apply_loaded_state()
        else:
            print(f"[Preset] Fehler: {path} nicht gefunden")

    def apply_loaded_state(self):
        print("[Preset] Werte übernommen:", self.sculpt_data)

    def refresh_layers(self):
        print("[Anatomie] Aktueller Zustand:", self.anatomy_state)
