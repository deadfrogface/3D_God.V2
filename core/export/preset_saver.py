import json
import os

class PresetSaver:
    def __init__(self, preset_dir="exports/presets/"):
        self.preset_dir = preset_dir
        os.makedirs(self.preset_dir, exist_ok=True)

    def save(self, character_data):
        name = character_data.get("name", "unbenannt")
        filename = f"{name.lower().replace(' ', '_')}.json"
        path = os.path.join(self.preset_dir, filename)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(character_data, f, indent=2)

        print(f"💾 Preset gespeichert: {path}")
        return path
