import json
import subprocess
import os
from core.logger import log

def open_blender_sculpt(file_path="blender_embed/sculpt_main.py"):
    log.info("[SculptToolBridge][open_blender_sculpt] ▶️ Versuche Blender mit Skript zu starten...")
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            blender_exe = config.get("blender_path", "blender.exe")
            log.info(f"[SculptToolBridge][open_blender_sculpt] ✅ Blender-Pfad geladen: {blender_exe}")
    except Exception as e:
        log.error(f"[SculptToolBridge][open_blender_sculpt] ❌ Fehler beim Laden der config.json: {e}")
        return

    script_path = os.path.abspath(file_path)
    if not os.path.exists(blender_exe):
        log.error(f"[SculptToolBridge][open_blender_sculpt] ❌ Fehler: Blender nicht gefunden unter {blender_exe}")
        return

    log.info(f"[SculptToolBridge][open_blender_sculpt] 🚀 Starte Blender mit: {script_path}")
    try:
        subprocess.run([
            blender_exe,
            "--background",
            "--python", script_path
        ])
        log.success("[SculptToolBridge][open_blender_sculpt] ✅ Blender-Skript ausgeführt")
    except Exception as e:
        log.error(f"[SculptToolBridge][open_blender_sculpt] ❌ Fehler beim Starten von Blender: {e}")