import os
import sys
import subprocess
import json

CHARMORPH_PATH = os.path.join(os.path.dirname(__file__), "../../CharMorph-master/generate_shape.py")

def run_charmorph(prompt=None):
    print(f"[CharMorph][run_charmorph] ▶️ Eingabe: prompt = {prompt}")
    try:
        prompt_arg = prompt if prompt else ""
        print("[CharMorph][run_charmorph] ⚡ Starte Morph-Generierung...")

        result = subprocess.run(
            [sys.executable, CHARMORPH_PATH, prompt_arg],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"[CharMorph][run_charmorph] ❌ Fehler: {result.stderr.strip()}")
            return None

        data = json.loads(result.stdout.strip())
        print(f"[CharMorph][run_charmorph] ✅ Erfolg: Daten erhalten – {data}")
        return data

    except Exception as e:
        print(f"[CharMorph][run_charmorph] ❌ Ausnahme: {e}")
        return None