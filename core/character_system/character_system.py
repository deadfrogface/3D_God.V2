import json
from pathlib import Path

class CharacterSystem:
    def __init__(self):
        self.nsfw_enabled = True
        self.anatomy_state = {}     # z. B. {"skin": True, "muscle": True}
        self.sculpt_data = {}       # z. B. {"torso_width": 1.2, "arm_length": 0.9}
        self.preset_path = Path("assets/character_presets/")
        self.preset_path.mkdir(parents=True, exist_ok=True)

    def set_nsfw_mode(self, enabled: bool):
        self.nsfw_enabled = enabled
        print(f"[System] 🔞 NSFW-Modus: {'An' if enabled else 'Aus'}")

    def new_character(self):
        print("[System] 🆕 Neuer Charakter erstellt")
        self.anatomy_state = {}
        self.sculpt_data = {}

    def load_preset(self, name: str) -> bool:
        path = self.preset_path / f"{name.lower()}.json"
        if not path.exists():
            print(f"❌ Preset nicht gefunden: {path}")
            return False

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.nsfw_enabled = data.get("nsfw", True)
        self.anatomy_state = data.get("anatomy", {})
        self.sculpt_data = data.get("sculpted", {})

        print(f"✅ Preset geladen: {name}")
        return True

    def save_preset(self, name: str = "custom") -> Path:
        path = self.preset_path / f"{name.lower()}.json"
        data = {
            "name": name,
            "nsfw": self.nsfw_enabled,
            "anatomy": self.anatomy_state,
            "sculpted": self.sculpt_data
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Preset gespeichert: {path}")
        return path

    def export_fbx(self):
        print("📤 Exportiere FBX... [Stub]")
        # TODO: Blender-Export oder anderes Tool anschließen