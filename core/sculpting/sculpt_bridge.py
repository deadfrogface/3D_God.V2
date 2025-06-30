import subprocess
import os
from pathlib import Path

class SculptTools:
    def __init__(self):
        self.blender_path = Path("blender_embedded/blender_3.6_portable/blender.exe").resolve()
        self.blend_file = Path("assets/base_bodies/female_base.blend").resolve()

    def launch(self):
        """Starte Blender manuell"""
        if not self.blender_path.exists() or not self.blend_file.exists():
            print("❌ Blender oder .blend-Datei nicht gefunden!")
            return

        print("🚀 Starte Blender...")
        subprocess.Popen([str(self.blender_path), str(self.blend_file)])

    def run_script(self, script_name: str):
        """Starte Blender-Skript im Hintergrund"""
        script_path = Path("blender_embedded/scripts") / script_name
        if not script_path.exists():
            print(f"❌ Skript fehlt: {script_path}")
            return

        cmd = [
            str(self.blender_path),
            "--background",
            str(self.blend_file),
            "--python", str(script_path.resolve())
        ]

        print(f"🧠 Führe Skript aus: {script_path.name}")
        subprocess.run(cmd)

    def apply_symmetry(self, axis: str = "X"):
        """Placeholder für spätere Blender-Symmetrie"""
        print(f"🔁 Symmetrie anwenden (Stub): Achse {axis}")