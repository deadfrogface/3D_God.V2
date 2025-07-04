import subprocess
import json
import os

class CharMorphHandler:
    def __init__(self):
        self.model_path = "CharMorph-master/"
        self.output_file = os.path.join(self.model_path, "output_shape.json")
        print("[AI][CharMorphHandler.__init__] ✅ Initialisiert")

    def generate_shape(self, prompt="muscular orc female"):
        print(f"[AI][CharMorphHandler.generate_shape] ▶️ Eingabe: prompt = '{prompt}'")
        try:
            subprocess.run([
                "python",
                os.path.join(self.model_path, "generate_shape.py"),
                "--prompt", prompt
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[AI][CharMorphHandler.generate_shape] ❌ Fehler beim Aufruf: {e}")
            return None

        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"[AI][CharMorphHandler.generate_shape] ✅ Shape erhalten: {data}")
                return data
            except Exception as e:
                print(f"[AI][CharMorphHandler.generate_shape] ❌ Fehler beim Parsen der Ausgabe: {e}")
                return None
        else:
            print("[AI][CharMorphHandler.generate_shape] ❌ Fehler: Ausgabedatei nicht gefunden")
            return None