import os
import subprocess
from core.character_system.character_system import CharacterSystem

class TripoSRHandler:
    def __init__(self):
        self.image_path = None
        self.preview_path = "exports/triposr_output/preview.png"

    def set_input_image(self, path):
        self.image_path = path
        print(f"[TripoSR] Bild gesetzt: {path}")

    def generate_mesh(self):
        if not self.image_path:
            print("[TripoSR] Kein Bild ausgewählt.")
            return

        print(f"[TripoSR] Starte Mesh-Erzeugung aus: {self.image_path}")
        subprocess.run([
            "python", "TripoSR-main/infer.py",
            "--config", "TripoSR-main/configs/config.yaml",
            "--image", self.image_path,
            "--output_dir", "exports/triposr_output"
        ])

        # Wenn Vorschau existiert → direkt anzeigen
        if os.path.exists(self.preview_path):
            print("[TripoSR] Vorschaubild gefunden – wird im Viewport angezeigt.")
            cs = CharacterSystem()
            if hasattr(cs, "viewport_ref") and cs.viewport_ref:
                cs.viewport_ref.update_preview_from_image(self.preview_path)
        else:
            print("[TripoSR] Kein Vorschaubild gefunden.")