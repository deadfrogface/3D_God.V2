import os
import json
import subprocess
from core.sculpting.sculpt_tool_bridge import SculptTools

class CharacterSystem:
    def __init__(self):
        self.config_path = "config.json"
        self.preset_path = "presets/"
        self.sculpt_data = {
            "height": 50,
            "breast_size": 50,
            "hip_width": 50,
            "arm_length": 50,
            "leg_length": 50,
            "symmetry": True
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
        self.physics_flags = {
            "breasts": True,
            "cloth": True,
            "piercings": True
        }
        self.materials = {
            "skin": {"color": "#f5cba7", "roughness": 0.5, "metallic": 0.0, "texture": ""},
            "clothes": {"color": "#cccccc", "roughness": 0.7, "metallic": 0.0, "texture": ""},
            "piercings": {"color": "#aaaaaa", "roughness": 0.1, "metallic": 1.0, "texture": ""},
            "tattoos": {"color": "#000000", "roughness": 0.9, "metallic": 0.0, "texture": ""}
        }
        self.config = self.load_config()
        self.sculpt_tools = SculptTools()
        self.nsfw_enabled = self.config.get("nsfw_enabled", True)
        self.viewport_ref = None

        # UI-Kontroll-Rückbindungen
        self.slider_sync_callback = None
        self.anatomy_sync_callback = None
        self.nsfw_sync_callback = None

    def load_config(self):
        if not os.path.exists(self.config_path):
            return {"theme": "dark", "nsfw_enabled": True, "controller_enabled": True, "debug_enabled": True}
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
        self.sculpt_tools.send_data(self.sculpt_data)
        self.sculpt_tools.launch()

    def export_model(self):
        print("[CharSystem] Exportiere Modell als FBX...")
        self.export_fbx("exported_character")

    def export_fbx(self, filename="exported_character"):
        print(f"[Export] Starte FBX-Export als {filename}.fbx ...")
        try:
            subprocess.run([
                self.config.get("blender_path", "blender"),
                "--background",
                "--python", os.path.join("blender_embed", "export_fbx.py"),
                "--", filename
            ])
            print("[Export] FBX erfolgreich abgeschlossen.")
        except Exception as e:
            print(f"[Export] Fehler: {e}")

    def update_anatomy_layer(self, layer_name, state):
        self.anatomy_state[layer_name] = state
        print(f"[Anatomie] Layer {layer_name} → {'On' if state else 'Off'}")
        self.refresh_layers()

    def add_asset(self, category):
        if category not in self.asset_state:
            print(f"[Asset] Ungültige Kategorie: {category}")
            return
        example_asset = f"{category}_demo_asset"
        self.asset_state[category].append(example_asset)
        print(f"[Asset] {category}: {example_asset} hinzugefügt")
        self.refresh_layers()

    def refresh_layers(self):
        print("[System] Viewport-Refresh wird ausgeführt...")
        print(" - Anatomie:", self.anatomy_state)
        print(" - Assets:", self.asset_state)
        if self.viewport_ref:
            self.viewport_ref.update_preview(self.anatomy_state, self.asset_state)

    def bind_viewport(self, viewport):
        self.viewport_ref = viewport

    def save_preset(self, name="default"):
        if not os.path.exists(self.preset_path):
            os.makedirs(self.preset_path)
        path = os.path.join(self.preset_path, f"{name}.json")
        with open(path, "w") as f:
            json.dump({
                "sculpt_data": self.sculpt_data,
                "nsfw": self.nsfw_enabled,
                "anatomy": self.anatomy_state,
                "assets": self.asset_state,
                "physics": self.physics_flags,
                "materials": self.materials
            }, f, indent=4)
        print(f"[Preset] Gespeichert: {path}")

    def load_preset(self, name="default"):
        path = os.path.join(self.preset_path, f"{name}.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.sculpt_data = data.get("sculpt_data", self.sculpt_data)
                self.nsfw_enabled = data.get("nsfw", self.nsfw_enabled)
                self.anatomy_state = data.get("anatomy", self.anatomy_state)
                self.asset_state = data.get("assets", self.asset_state)
                self.physics_flags = data.get("physics", self.physics_flags)
                self.materials = data.get("materials", self.materials)
            self.apply_loaded_state()
        else:
            print(f"[Preset] Fehler: {path} nicht gefunden")

    def apply_loaded_state(self):
        print("[Preset] Zustand übernommen.")
        print(" - Sculpt:", self.sculpt_data)
        print(" - Anatomy:", self.anatomy_state)
        print(" - Assets:", self.asset_state)

        self.refresh_layers()

        if self.slider_sync_callback:
            self.slider_sync_callback()
        if self.anatomy_sync_callback:
            self.anatomy_sync_callback()
        if self.nsfw_sync_callback:
            self.nsfw_sync_callback()
        if self.viewport_ref:
            self.viewport_ref.update_view()