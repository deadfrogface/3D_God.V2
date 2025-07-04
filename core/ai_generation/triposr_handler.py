import os
import subprocess
from core.character_system.character_system import CharacterSystem

class TripoSRHandler:
    def __init__(self):
        print("[TripoSRHandler][__init__] ▶️ Initialisiert")
        self.image_path = None
        self.preview_path = "exports/triposr_output/preview.png"
        print("[TripoSRHandler][__init__] ✅ Handler bereit")

    def set_input_image(self, path):
        print(f"[TripoSRHandler][set_input_image] ▶️ Eingabe: path={path}")
        self.image_path = path
        print(f"[TripoSRHandler][set_input_image] ✅ Bild gesetzt: {path}")

    def generate_mesh(self):
        print(f"[TripoSRHandler][generate_mesh] ▶️ Start mit image_path={self.image_path}")
        if not self.image_path:
            print("[TripoSRHandler][generate_mesh] ❌ Kein Bild ausgewählt.")
            return

        try:
            print(f"[TripoSRHandler][generate_mesh] 🔄 Starte Mesh-Erzeugung...")
            subprocess.run([
                "python", "TripoSR-main/infer.py",
                "--config", "TripoSR-main/configs/config.yaml",
                "--image", self.image_path,
                "--output_dir", "exports/triposr_output"
            ], check=True)
            print(f"[TripoSRHandler][generate_mesh] ✅ Mesh-Erzeugung abgeschlossen")
        except subprocess.CalledProcessError as e:
            print(f"[TripoSRHandler][generate_mesh] ❌ Fehler beim Ausführen von infer.py: {e}")
            return

        if os.path.exists(self.preview_path):
            print("[TripoSRHandler][generate_mesh] ✅ Vorschau gefunden – lade in Viewport")
            cs = CharacterSystem()
            if hasattr(cs, "viewport_ref") and cs.viewport_ref:
                cs.viewport_ref.update_preview_from_image(self.preview_path)
            else:
                print("[TripoSRHandler][generate_mesh] ⚠️ Kein aktiver Viewport verbunden")
        else:
            print("[TripoSRHandler][generate_mesh] ❌ Kein Vorschaubild gefunden.")