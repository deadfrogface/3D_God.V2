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
            "organs": False,
            "breasts": True,
            "genitals": True,
            "bodyhair": False
        }
        self.asset_state = {
            "clothes": [],
            "piercings": [],
            "tattoos": []
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

    def sculpt(self):
        print("[Sculpt] Blender Sculpting wird gestartet...")
        self.sculpt_tools.launch()

    def run_blender_script(self, script_name):
        print(f"[Sculpt] Führe Blender-Skript aus: {script_name}")
        self.sculpt_tools.run_script(script_name)

    def update_anatomy_layer(self, layer_name, state):
        self.anatomy_state[layer_name] = state
        print(f"[Anatomie] Layer {layer_name} → {'On' if state else 'Off'}")

    def refresh_layers(self):
        print("[Anatomie] Aktueller Zustand:", self.anatomy_state)

    def add_asset(self, category):
        if category not in self.asset_state:
            print(f"[Asset] Ungültige Kategorie: {category}")
            return
        example_asset = f"{category}_demo_asset"
        self.asset_state[category].append(example_asset)
        print(f"[Asset] {category}: {example_asset} hinzugefügt")

    def save_preset(self, name="default"):
        if not os.path.exists(self.preset_path):
            os.makedirs(self.preset_path)
        path = os.path.join(self.preset_path, f"{name}.json")
        with open(path, "w") as f:
            json.dump({
                "sculpt_data": self.sculpt_data,
                "nsfw": self.nsfw_enabled,
                "anatomy": self.anatomy_state,
                "assets": self.asset_state
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
                self.asset_state = data.get("assets", {})
            self.apply_loaded_state()
        else:
            print(f"[Preset] Fehler: {path} nicht gefunden")

    def apply_loaded_state(self):
        print("[Preset] Werte übernommen:", self.sculpt_data)
        print("[Preset] Assets:", self.asset_state)
        self.refresh_layers()
def export_fbx(self, filename="exported_character"):
        script_name = "export_fbx.py"
        self.run_blender_script(script_name + f" {filename}")