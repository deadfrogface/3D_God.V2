import json
import os
import subprocess

class CharacterSystem:
    def __init__(self):
        self.anatomy_state = {
            "skin": True,
            "fat": True,
            "muscles": True,
            "bones": False,
            "organs": False,
        }

        self.sculpt_data = {
            "height": 50,
            "breast_size": 50,
            "hip_width": 50,
            "arm_length": 50,
            "leg_length": 50,
        }

        self.symmetry = True
        self.slider_sync_callback = None  # ← für Block 57

    def update_anatomy_state(self, layer, state):
        self.anatomy_state[layer] = state

    def update_sculpt_value(self, key, value):
        self.sculpt_data[key] = value

    def start_sculpting(self):
        print("🔧 Sculpting gestartet...")
        with open("config.json") as f:
            config = json.load(f)
        blender_exe = config.get("blender_path", "blender")
        script_path = os.path.join("blender_embed", "sculpt_tool_bridge.py")

        try:
            subprocess.run([blender_exe, "--background", "--python", script_path])
            print("✅ Sculpting abgeschlossen.")
        except Exception as e:
            print(f"❌ Fehler beim Sculpting: {e}")

    def export_fbx(self, filename):
        print(f"📤 Exportiere {filename}.fbx ...")
        with open("config.json") as f:
            config = json.load(f)
        blender_exe = config.get("blender_path", "blender")
        script_path = os.path.join("blender_embed", "export_fbx.py")

        try:
            subprocess.run([
                blender_exe,
                "--background",
                "--python", script_path,
                "--", filename
            ])
            print("✅ FBX exportiert.")
        except Exception as e:
            print(f"❌ Fehler beim Export: {e}")

    def save_preset(self, name):
        preset = {
            "anatomy": self.anatomy_state,
            "sculpt": self.sculpt_data,
        }
        os.makedirs("presets", exist_ok=True)
        with open(f"presets/{name}.json", "w") as f:
            json.dump(preset, f, indent=4)

    def load_preset(self, name):
        path = f"presets/{name}.json"
        if not os.path.exists(path):
            print(f"❌ Preset {name} nicht gefunden.")
            return
        with open(path, "r") as f:
            preset = json.load(f)
        self.apply_loaded_state(preset)

    def apply_loaded_state(self, preset):
        self.anatomy_state = preset.get("anatomy", self.anatomy_state)
        self.sculpt_data = preset.get("sculpt", self.sculpt_data)
        if self.slider_sync_callback:
            self.slider_sync_callback()