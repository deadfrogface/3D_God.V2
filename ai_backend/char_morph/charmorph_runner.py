import os
import sys
import subprocess
import json

CHARMORPH_PATH = os.path.join(os.path.dirname(__file__), "../../CharMorph-master/generate_shape.py")

def run_charmorph(prompt=None):
    try:
        prompt_arg = prompt if prompt else ""
        print("[CharMorph] Starte Morph-Generierung...")
        result = subprocess.run(
            [sys.executable, CHARMORPH_PATH, prompt_arg],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            print("[CharMorph] Fehler:", result.stderr)
            return None
        return json.loads(result.stdout.strip())
    except Exception as e:
        print(f"[CharMorph] Ausnahme: {e}")
        return None