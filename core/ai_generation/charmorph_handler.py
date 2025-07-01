import subprocess
import json
import os

class CharMorphHandler:
    def __init__(self):
        self.model_path = "CharMorph-master/"
        self.output_file = os.path.join(self.model_path, "output_shape.json")

    def generate_shape(self, prompt="muscular orc female"):
        print(f"[CharMorph] Sende Prompt: {prompt}")
        subprocess.run([
            "python",
            os.path.join(self.model_path, "generate_shape.py"),
            "--prompt", prompt
        ])

        if os.path.exists(self.output_file):
            with open(self.output_file, "r") as f:
                data = json.load(f)
                print("[CharMorph] Shape erfolgreich empfangen:", data)
                return data
        else:
            print("[CharMorph] Fehler: Keine Ausgabe erhalten")
            return None