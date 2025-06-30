import json
import os

class PresetHandler:
    def __init__(self, preset_dir="assets/character_presets/"):
        self.preset_dir = preset_dir
        os.makedirs(preset_dir, exist_ok=True)

    def save_preset(self, name, character_data: dict):
        path = os.path.join(self.preset_dir, f"{name.lower()}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, indent=2)
        print(f"✅ Preset gespeichert: {path}")

    def load_preset(self, name) -> dict:
        path = os.path.join(self.preset_dir, f"{name.lower()}.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Preset geladen: {path}")
            return data
        else:
            print(f"❌ Preset nicht gefunden: {path}")
            return None
