import os
import json
import subprocess
from core.logger import log
from core.sculpting.sculpt_tool_bridge import SculptTools

class CharacterSystem:
    def __init__(self):
        log.info("[CharacterSystem][__init__] ▶️ Initialisierung gestartet")
        self.config_path = "config.json"
        self.preset_path = "presets/"

        self.sculpt_data = {
            "height": 50, "breast_size": 50, "hip_width": 50,
            "arm_length": 50, "leg_length": 50, "symmetry": True
        }
        self.anatomy_state = {
            "skin": True, "fat": True, "muscle": False, "bone": False,
            "organs": False, "breasts": True, "genitals": True, "bodyhair": False
        }
        self.asset_state = {
            "clothes": [], "piercings": [], "tattoos": []
        }
        self.physics_flags = {
            "breasts": True, "cloth": True, "piercings": True
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

        self.slider_sync_callback = None
        self.anatomy_sync_callback = None
        self.nsfw_sync_callback = None

        # Standardmodell laden, wenn kein Preset existiert
        if not os.path.exists(os.path.join(self.preset_path, "default.json")):
            self.load_base_model("male")

        log.success("[CharacterSystem][__init__] ✅ Initialisierung abgeschlossen")

    def load_config(self):
        log.info("[CharacterSystem][load_config] ▶️ Lädt Konfiguration")
        if not os.path.exists(self.config_path):
            log.warning("[CharacterSystem][load_config] ❗ Standardkonfiguration geladen")
            return {"theme": "dark", "nsfw_enabled": True, "controller_enabled": True, "debug_enabled": True}
        with open(self.config_path, "r") as f:
            config = json.load(f)
            log.success("[CharacterSystem][load_config] ✅ Konfiguration geladen")
            return config

    def save_config(self):
        log.info("[CharacterSystem][save_config] ▶️ Speichert Konfiguration")
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
        log.success("[CharacterSystem][save_config] ✅ Konfiguration gespeichert")

    def update_sculpt_value(self, key, value):
        log.info(f"[CharacterSystem][update_sculpt_value] ▶️ {key} = {value}")
        self.sculpt_data[key] = value
        self.sculpt_tools.send_data(self.sculpt_data)  # 🟢 Direkt an Blender senden
        self.refresh_layers()                          # 🔁 Viewport updaten

    def sculpt(self):
        log.info("[CharacterSystem][sculpt] ▶️ Starte Blender Sculpting")
        self.sculpt_tools.send_data(self.sculpt_data)
        self.sculpt_tools.launch()

    def export_model(self):
        log.info("[CharacterSystem][export_model] ▶️ Exportiere Modell als FBX")
        self.export_fbx("exported_character")

    def export_fbx(self, filename="exported_character"):
        log.info(f"[CharacterSystem][export_fbx] ▶️ Starte Export für {filename}.fbx")
        try:
            subprocess.run([
                self.config.get("blender_path", "blender"),
                "--background",
                "--python", os.path.join("blender_embed", "export_fbx.py"),
                "--", filename
            ])
            log.success("[CharacterSystem][export_fbx] ✅ Export abgeschlossen")
        except Exception as e:
            log.error(f"[CharacterSystem][export_fbx] ❌ Fehler: {e}")

    def update_anatomy_layer(self, layer_name, state):
        log.info(f"[CharacterSystem][update_anatomy_layer] ▶️ {layer_name} = {state}")
        self.anatomy_state[layer_name] = state
        self.refresh_layers()

    def add_asset(self, category):
        log.info(f"[CharacterSystem][add_asset] ▶️ Kategorie: {category}")
        if category not in self.asset_state:
            log.error(f"[CharacterSystem][add_asset] ❌ Ungültige Kategorie: {category}")
            return
        example_asset = f"{category}_demo_asset"
        self.asset_state[category].append(example_asset)
        log.success(f"[CharacterSystem][add_asset] ✅ Hinzugefügt: {example_asset}")
        self.refresh_layers()

    def refresh_layers(self):
        log.info("[CharacterSystem][refresh_layers] ▶️ Aktualisiere Viewport")
        log.debug(f" - Anatomie: {self.anatomy_state}")
        log.debug(f" - Assets: {self.asset_state}")
        if self.viewport_ref:
            self.viewport_ref.update_preview(self.anatomy_state, self.asset_state)

    def bind_viewport(self, viewport):
        log.info("[CharacterSystem][bind_viewport] ▶️ Binde Viewport")
        self.viewport_ref = viewport

    def save_preset(self, name="default"):
        log.info(f"[CharacterSystem][save_preset] ▶️ Speichert Preset: {name}")
        os.makedirs(self.preset_path, exist_ok=True)
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
        log.success(f"[CharacterSystem][save_preset] ✅ Gespeichert unter: {path}")

    def load_preset(self, name="default"):
        log.info(f"[CharacterSystem][load_preset] ▶️ Lade Preset: {name}")
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
            log.success("[CharacterSystem][load_preset] ✅ Preset geladen")
            self.apply_loaded_state()
        else:
            log.error(f"[CharacterSystem][load_preset] ❌ Nicht gefunden: {path}")

    def apply_loaded_state(self):
        log.info("[CharacterSystem][apply_loaded_state] ▶️ Übernehme geladenen Zustand")
        log.debug(f" - Sculpt: {self.sculpt_data}")
        log.debug(f" - Anatomy: {self.anatomy_state}")
        log.debug(f" - Assets: {self.asset_state}")
        self.refresh_layers()
        if self.slider_sync_callback:
            self.slider_sync_callback()
        if self.anatomy_sync_callback:
            self.anatomy_sync_callback()
        if self.nsfw_sync_callback:
            self.nsfw_sync_callback()
        if self.viewport_ref:
            self.viewport_ref.update_view()

    def generate_ai_morph(self, prompt=None):
        from ai_backend.char_morph.charmorph_runner import run_charmorph
        log.info(f"[CharacterSystem][generate_ai_morph] ▶️ Prompt: {prompt or '–'}")
        result = run_charmorph(prompt)
        if not result:
            log.error("[CharacterSystem][generate_ai_morph] ❌ Kein Ergebnis erhalten")
            return
        for key in self.sculpt_data:
            if key in result:
                self.sculpt_data[key] = result[key]
                log.debug(f"[CharacterSystem][generate_ai_morph] {key} → {result[key]}")
        if self.slider_sync_callback:
            self.slider_sync_callback()

    def load_base_model(self, gender="male"):
        log.info(f"[CharacterSystem][load_base_model] ▶️ Lade Basis-Modell ({gender})")
        path = f"assets/characters/{gender}_base.glb"
        if os.path.exists(path):
            if self.viewport_ref:
                self.viewport_ref.load_preview(path)
            log.success(f"[CharacterSystem][load_base_model] ✅ Geladen: {path}")
        else:
            log.error(f"[CharacterSystem][load_base_model] ❌ Nicht gefunden: {path}")
