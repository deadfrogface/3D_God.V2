import os
import sys
import subprocess
import json
from core.logger import log

CHARMORPH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../CharMorph-master/generate_shape.py"))

def run_charmorph(prompt=None):
    log.info(f"[CharMorph][run_charmorph] ▶️ Eingabe: prompt = {prompt}")
    try:
        if not os.path.exists(CHARMORPH_PATH):
            raise FileNotFoundError(f"[CharMorph] ❌ Script nicht gefunden: {CHARMORPH_PATH}")

        prompt_arg = prompt if prompt else ""
        log.info("[CharMorph][run_charmorph] ⚡ Starte Morph-Generierung...")

        result = subprocess.run(
            [sys.executable, CHARMORPH_PATH, prompt_arg],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            log.error(f"[CharMorph][run_charmorph] ❌ Fehler: {result.stderr.strip()}")
            return None

        data = json.loads(result.stdout.strip())
        log.success(f"[CharMorph][run_charmorph] ✅ Erfolg: Daten erhalten – {data}")
        return data

    except Exception as e:
        log.error(f"[CharMorph][run_charmorph] ❌ Ausnahme: {e}")
        return None
