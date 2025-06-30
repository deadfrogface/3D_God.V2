import subprocess
import os
from pathlib import Path

class SculptTools:
    def __init__(self):
        self.blender_path = Path("blender_embedded/blender_3.6_portable/blender.exe").resolve()
        self.blend_file = Path("assets/base_bodies/female_base.blend").resolve()  # Standard-Charakter

    def launch(self):
        """Starte Blender GUI für Sculpting"""
        if not self.blender_path.exists() or not self.blend_file.exists():
            print("❌ Blender oder .blend-Datei nicht gefunden!")
            return

        print("🚀 Starte Blender für Sculpting...")
        subprocess.Popen([str(self.blender_path), str(self.blend_file)])

    def run_script(self, script_name: str):
        """Führe ein Blender-Skript aus"""
        script_path = Path("blender_embedded/scripts") / script_name
        if not script_path.exists():
            print(f"❌ Blender-Skript nicht gefunden: {script_path}")
            return

        cmd = [
            str(self.blender_path),
            "--background",
            str(self.blend_file),
            "--python", str(script_path.resolve())
        ]

        print(f"⚙️ Führe Blender-Skript aus: {script_name}")
        subprocess.run(cmd)

    def apply_symmetry(self, axis: str = "X"):
        """Stub: Symmetrie in Blender anwenden"""
        print(f"🔁 Symmetrie anwenden: {axis}")
        # In Zukunft könnte man `symmetry_axis = axis` als Umgebungsvariable setzen
        # oder direkt in ein temp-Skript einfügen