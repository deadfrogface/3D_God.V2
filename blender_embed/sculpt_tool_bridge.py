import json
import subprocess
import os

def open_blender_sculpt(file_path="blender_embed/sculpt_main.py"):
    with open("config.json") as config_file:
        config = json.load(config_file)
        blender_exe = config.get("blender_path", "blender.exe")

    script_path = os.path.abspath(file_path)
    if not os.path.exists(blender_exe):
        print(f"[SculptToolBridge] Fehler: Blender nicht gefunden unter {blender_exe}")
        return

    print(f"[SculptToolBridge] Starte Blender mit Skript: {script_path}")
    subprocess.run([blender_exe, "--background", "--python", script_path])