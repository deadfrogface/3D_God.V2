import json
import os

class PresetSaver:
    def __init__(self, preset_dir="exports/presets/"):
        print(f"[PresetSaver][__init__] ▶️ Eingabe: preset_dir={preset_dir}")
        self.preset_dir = preset_dir
        os.makedirs(self.preset_dir, exist_ok=True)
        print("[PresetSaver][__init__] ✅ Ordner angelegt (falls nicht vorhanden)")

    def save(self, character_data):
        print(f"[PresetSaver][save] ▶️ Eingabe: character_data={character_data}")
        name = character_data.get("name", "unbenannt")
        filename = f"{name.lower().replace(' ', '_')}.json"
        path = os.path.join(self.preset_dir, filename)

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(character_data, f, indent=2)
            print(f"[PresetSaver][save] ✅ Preset gespeichert: {path}")
            return path
        except Exception as e:
            print(f"[PresetSaver][save] ❌ Fehler beim Speichern: {e}")
            return None