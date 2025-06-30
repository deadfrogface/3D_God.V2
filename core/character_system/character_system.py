import json
import os
import subprocess
from pathlib import Path

class CharacterSystem:
    def __init__(self):
        self.nsfw_enabled = True
        self.anatomy_state = {}     # z. B. {"skin": True, "muscle": True}
        self.sculpt_data = {}       # z. B. {"torso_width": 1.2, "arm_length": 0.9}
        self.preset_path = Path("assets/character_presets/")
        self.preset_path.mkdir(parents=True, exist_ok=True)
        Path("exports").mkdir(exist_ok=True)

        # Optional: Sculpting-Objekt vorbereiten
        try:
            from core.sculpting.sculpt_bridge import SculptTools
            self.sculpt_tools = SculptTools()
        except Exception as e:
            print(f"[System] ⚠️ SculptTools konnte nicht geladen werden: {e}")
            self.sculpt_tools = None

    def set_nsfw_mode(self, enabled: bool):
        self.nsfw_enabled = enabled
        print(f"[System] 🔞 NSFW-Modus: {'An' if enabled else 'Aus'}")

    def new_character(self):
        print("[System] 🆕 Neuer Charakter erstellt")
        self.anatomy_state = {}
        self.sculpt_data = {}

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

    def sculpt(self):
        print("🎨 Starte Sculpting...")
        if self.sculpt_tools:
            self.sculpt_tools.launch()

    def run_blender_script(self, script_name: str):
        print(f"🧠 Führe Blender-Skript aus: {script_name}")
        if self.sculpt_tools:
            self.sculpt_tools.run_script(script_name)

    def export_fbx(self):
        output_path = Path("exports/character.fbx").resolve()
        export_script = Path("blender_embedded/scripts/export_fbx.py").resolve()

        if not export_script.exists():
            print("❌ Export-Skript fehlt!")
            return

        if not self.sculpt_tools:
            print("❌ SculptTools nicht verfügbar!")
            return

        cmd = [
            str(self.sculpt_tools.blender_path),
            "--background",
            str(self.sculpt_tools.blend_file),
            "--python", str(export_script)
        ]

        env = dict(**os.environ, FBX_EXPORT_PATH=str(output_path))

        print(f"📦 Starte FBX-Export nach: {output_path}")
        subprocess.run(cmd, env=env)