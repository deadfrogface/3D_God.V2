import os
import subprocess
import sys
import json

def morph_from_prompt(prompt: str = "") -> dict | None:
    """
    Führt char_morph_generate_shape.py mit einem Prompt aus und gibt die Formdaten zurück.

    :param prompt: Beschreibung des gewünschten Charakters (z. B. "slim orc assassin")
    :return: Dictionary mit generierten Proportionen oder None bei Fehler
    """
    script_path = os.path.join(os.path.dirname(__file__), "char_morph_generate_shape.py")

    if not os.path.isfile(script_path):
        print(f"❌ Script nicht gefunden: {script_path}")
        return None

    try:
        result = subprocess.run(
            [sys.executable, script_path, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print("❌ Fehler bei CharMorph:")
            print(result.stderr.strip())
            return None

        output = json.loads(result.stdout.strip())
        print("✅ Erfolgreich generiert:", output)
        return output

    except Exception as e:
        print("❌ Ausnahme in CharMorph:", e)
        return None
