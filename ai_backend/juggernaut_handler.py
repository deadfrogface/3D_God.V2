import subprocess
import os

class JuggernautHandler:
    def __init__(self):
        self.script_path = "external/juggernaut/run.py"
        self.output_path = "exports/juggernaut_output"
        os.makedirs(self.output_path, exist_ok=True)
        print("[JuggernautHandler][__init__] ✅ Initialisiert")

    def run(self, input_path):
        print(f"[JuggernautHandler][run] ▶️ Eingabe: {input_path}")
        try:
            subprocess.run([
                "python", self.script_path,
                "--input", input_path,
                "--output", self.output_path
            ], check=True)
            print(f"[JuggernautHandler][run] ✅ Erfolgreich abgeschlossen → {self.output_path}")
        except subprocess.CalledProcessError as e:
            print(f"[JuggernautHandler][run] ❌ Fehler bei der Ausführung: {e}")
        except Exception as e:
            print(f"[JuggernautHandler][run] ❌ Unerwarteter Fehler: {e}")
