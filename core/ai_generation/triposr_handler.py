import os
import subprocess

class TripoSRHandler:
    def __init__(self):
        self.image_path = None

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