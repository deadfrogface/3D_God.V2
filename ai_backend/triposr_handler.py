import subprocess
import os

class TripoSRHandler:
    def __init__(self):
        self.triposr_path = "external/triposr"
        self.output_dir = "exports/triposr_output"
        os.makedirs(self.output_dir, exist_ok=True)
        print("[TripoSRHandler][__init__] ✅ Initialisiert")

    def run_triposr(self, image_path):
        print(f"[TripoSRHandler][run_triposr] ▶️ Eingabe: {image_path}")
        try:
            subprocess.run([
                "python", f"{self.triposr_path}/launch.py",
                "--image", image_path,
                "--output", self.output_dir
            ], check=True)
            print(f"[TripoSRHandler][run_triposr] ✅ 3D-Modell erstellt in {self.output_dir}")
        except subprocess.CalledProcessError as e:
            print(f"[TripoSRHandler][run_triposr] ❌ Fehler beim Ausführen von TripoSR: {e}")