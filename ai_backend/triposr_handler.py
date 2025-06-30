import subprocess, os

class TripoSRHandler:
    def __init__(self):
        self.triposr_path = "external/triposr"
        self.output_dir = "exports/triposr_output"
        os.makedirs(self.output_dir, exist_ok=True)

    def run_triposr(self, image_path):
        subprocess.run([
            "python", f"{self.triposr_path}/launch.py",
            "--image", image_path,
            "--output", self.output_dir
        ])
        print(f"3D-Modell erstellt in {self.output_dir}")

