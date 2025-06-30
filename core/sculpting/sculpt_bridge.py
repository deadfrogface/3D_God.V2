import subprocess
from pathlib import Path

class SculptTools:
    def __init__(self):
        self.blender_path = Path("blender_embedded/blender_3.6_portable/blender.exe")
        self.blend_file = Path("assets/base_bodies/female_base.blend")
        self.script_folder = Path("blender_embedded/scripts")

    def launch(self):
        """Starte Blender mit Sculpting-Modell"""
        if not self.blender_path.exists():
            print("❌ Blender nicht gefunden!")
            return

        cmd = [
            str(self.blender_path),
            str(self.blend_file)
        ]
        print(f"🚀 Starte Blender: {' '.join(cmd)}")
        subprocess.Popen(cmd)

    def run_script(self, script_name: str):
        """Führe externes Blender-Skript aus"""
        script = self.script_folder / script_name
        if not script.exists():
            print(f"❌ Blender-Skript fehlt: {script}")
            return

        cmd = [
            str(self.blender_path),
            "--background",
            str(self.blend_file),
            "--python", str(script)
        ]
        print(f"🧠 Führe Blender-Skript aus: {script.name}")
        subprocess.Popen(cmd)

    def apply_symmetry(self, axis: str = "X"):
        print(f"🔁 Symmetrie auf Achse {axis} anwenden... [Stub]")
        # Optional: später Blender-Befehl dafür einbauen