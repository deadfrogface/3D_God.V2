import os import json import subprocess from core.sculpting.sculpt_tool_bridge import SculptTools

class CharacterSystem: def init(self): print("[CharacterSystem][init] ▶️ Initialisierung gestartet") self.config_path = "config.json" self.preset_path = "presets/" self.sculpt_data = { "height": 50, "breast_size": 50, "hip_width": 50, "arm_length": 50, "leg_length": 50, "symmetry": True } self.anatomy_state = { "skin": True, "fat": True, "muscle": False, "bone": False, "organs": False, "breasts": True, "genitals": True, "bodyhair": False } self.asset_state = { "clothes": [], "piercings": [], "tattoos": [] } self.physics_flags = { "breasts": True, "cloth": True, "piercings": True } self.materials = { "skin": {"color": "#f5cba7", "roughness": 0.5, "metallic": 0.0, "texture": ""}, "clothes": {"color": "#cccccc", "roughness": 0.7, "metallic": 0.0, "texture": ""}, "piercings": {"color": "#aaaaaa", "roughness": 0.1, "metallic": 1.0, "texture": ""}, "tattoos": {"color": "#000000", "roughness": 0.9, "metallic": 0.0, "texture": ""} } self.config = self.load_config() self.sculpt_tools = SculptTools() self.nsfw_enabled = self.config.get("nsfw_enabled", True) self.viewport_ref = None

self.slider_sync_callback = None
    self.anatomy_sync_callback = None
    self.nsfw_sync_callback = None
    print("[CharacterSystem][__init__] ✅ Initialisierung abgeschlossen")

def load_config(self):
    print("[CharacterSystem][load_config] ▶️ Lädt Konfiguration")
    if not os.path.exists(self.config_path):
        print("[CharacterSystem][load_config] ❗ Standardkonfiguration geladen")
        return {"theme": "dark", "nsfw_enabled": True, "controller_enabled": True, "debug_enabled": True}
    with open(self.config_path, "r") as f:
        config = json.load(f)
        print("[CharacterSystem][load_config] ✅ Konfiguration geladen")
        return config

def save_config(self):
    print("[CharacterSystem][save_config] ▶️ Speichert Konfiguration")
    with open(self.config_path, "w") as f:
        json.dump(self.config, f, indent=4)
    print("[CharacterSystem][save_config] ✅ Konfiguration gespeichert")

def update_sculpt_value(self, key, value):
    print(f"[CharacterSystem][update_sculpt_value] ▶️ {key} = {value}")
    self.sculpt_data[key] = value

def sculpt(self):
    print("[CharacterSystem][sculpt] ▶️ Starte Blender Sculpting")
    self.sculpt_tools.send_data(self.sculpt_data)
    self.sculpt_tools.launch()

def export_model(self):
    print("[CharacterSystem][export_model] ▶️ Exportiere Modell als FBX")
    self.export_fbx("exported_character")

def export_fbx(self, filename="exported_character"):
    print(f"[CharacterSystem][export_fbx] ▶️ Starte Export für {filename}.fbx")
    try:
        subprocess.run([
            self.config.get("blender_path", "blender"),
            "--background",
            "--python", os.path.join("blender_embed", "export_fbx.py"),
            "--", filename
        ])
        print("[CharacterSystem][export_fbx] ✅ Export abgeschlossen")
    except Exception as e:
        print(f"[CharacterSystem][export_fbx] ❌ Fehler: {e}")

def update_anatomy_layer(self, layer_name, state):
    print(f"[CharacterSystem][update_anatomy_layer] ▶️ {layer_name} = {state}")
    self.anatomy_state[layer_name] = state
    self.refresh_layers()

def add_asset(self, category):
    print(f"[CharacterSystem][add_asset] ▶️ Kategorie: {category}")
    if category not in self.asset_state:
        print(f"[CharacterSystem][add_asset] ❌ Ungültige Kategorie: {category}")
        return
    example_asset = f"{category}_demo_asset"
    self.asset_state[category].append(example_asset)
    print(f"[CharacterSystem][add_asset] ✅ Hinzugefügt: {example_asset}")
    self.refresh_layers()

def refresh_layers(self):
    print("[CharacterSystem][refresh_layers] ▶️ Aktualisiere Viewport")
    print(" - Anatomie:", self.anatomy_state)
    print(" - Assets:", self.asset_state)
    if self.viewport_ref:
        self.viewport_ref.update_preview(self.anatomy_state, self.asset_state)

def bind_viewport(self, viewport):
    print("[CharacterSystem][bind_viewport] ▶️ Binde Viewport")
    self.viewport_ref = viewport

def save_preset(self, name="default"):
    print(f"[CharacterSystem][save_preset] ▶️ Speichert Preset: {name}")
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
    print(f"[CharacterSystem][save_preset] ✅ Gespeichert unter: {path}")

def load_preset(self, name="default"):
    print(f"[CharacterSystem][load_preset] ▶️ Lade Preset: {name}")
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
        print("[CharacterSystem][load_preset] ✅ Preset geladen")
        self.apply_loaded_state()
    else:
        print(f"[CharacterSystem][load_preset] ❌ Nicht gefunden: {path}")

def apply_loaded_state(self):
    print("[CharacterSystem][apply_loaded_state] ▶️ Übernehme geladenen Zustand")
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

def generate_ai_morph(self, prompt=None):
    from ai_backend.char_morph.charmorph_runner import run_charmorph
    print(f"[CharacterSystem][generate_ai_morph] ▶️ Prompt: {prompt or '–'}")
    result = run_charmorph(prompt)

    if not result:
        print("[CharacterSystem][generate_ai_morph] ❌ Kein Ergebnis erhalten")
        return

    for key in self.sculpt_data:
        if key in result:
            self.sculpt_data[key] = result[key]
            print(f"[CharacterSystem][generate_ai_morph] {key} → {result[key]}")

    if self.slider_sync_callback:
        self.slider_sync_callback()

