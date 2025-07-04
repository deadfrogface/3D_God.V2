import json
import os
from core.logger import log  # Logging importieren

class PresetHandler:
    def __init__(self, preset_dir="assets/character_presets/"):
        log.info(f"[PresetHandler][__init__] ▶️ Eingabe: preset_dir={preset_dir}")
        self.preset_dir = preset_dir
        os.makedirs(preset_dir, exist_ok=True)
        log.success(f"[PresetHandler][__init__] ✅ Verzeichnis vorbereitet: {self.preset_dir}")

    def save_preset(self, name, character_data: dict):
        log.info(f"[PresetHandler][save_preset] ▶️ Eingabe: name={name}")
        path = os.path.join(self.preset_dir, f"{name.lower()}.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(character_data, f, indent=2)
            log.success(f"[PresetHandler][save_preset] ✅ Preset gespeichert: {path}")
        except Exception as e:
            log.error(f"[PresetHandler][save_preset] ❌ Fehler beim Speichern: {e}")

    def load_preset(self, name) -> dict:
        log.info(f"[PresetHandler][load_preset] ▶️ Eingabe: name={name}")
        path = os.path.join(self.preset_dir, f"{name.lower()}.json")
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                log.success(f"[PresetHandler][load_preset] ✅ Preset geladen: {path}")
                return data
            except Exception as e:
                log.error(f"[PresetHandler][load_preset] ❌ Fehler beim Laden: {e}")
                return None
        else:
            log.warning(f"[PresetHandler][load_preset] ❌ Preset nicht gefunden: {path}")
            return None