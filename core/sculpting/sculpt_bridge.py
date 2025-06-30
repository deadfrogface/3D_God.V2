import subprocess
from pathlib import Path
import os

class SculptTools:
    def __init__(self):
        self.blender_path = Path("blender_embedded/blender_3.6_portable/blender.exe")
        self.blend_file = Path("assets/base_bodies/female_base.blend")
        self.script_dir = Path("blender_embedded/scripts/")

        # Sicherstellen, dass Pfade existieren
        if not self.script_dir.exists():
            self.script_dir.mkdir(parents=True, exist_ok=True)
        if not self.blend_file.exists():
            print(f"⚠️ Warnung: .blend Datei fehlt: {self.blend_file}")

    def launch(self):
        """Starte Blender mit Basis-Datei"""
        print("🧱 Starte Blender im GUI-Modus")
        cmd = [
            str(self.blender_path),
            str(self.blend_file)
        ]
        subprocess.run(cmd)

    def run_script(self, script_name):
        """Führe ein internes Blender-Skript aus (z. B. Symmetrie, Auto-Weight)"""
        script_path = self.script_dir / script_name
        if not script_path.exists():
            print(f"❌ Blender-Skript nicht gefunden: {script_path}")
            return

        print(f"🧠 Führe Blender im Hintergrund aus mit: {script_name}")
        cmd = [
            str(self.blender_path),
            "--background",
            str(self.blend_file),
            "--python", str(script_path)
        ]
        subprocess.run(cmd)
    
    def apply_symmetry(self, axis: str = "X"):
        """Optional: Achsensymmetrie anwenden"""
        print(f"🔁 Symmetrie anwenden entlang {axis}-Achse")
        self.run_script(f"symmetry_{axis.lower()}.py")