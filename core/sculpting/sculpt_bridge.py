import subprocess
import os

class SculptTools:
    def __init__(self):
        self.blender_path = "blender_embedded/blender_3.6_portable/blender.exe"
        self.blend_file = "assets/base_bodies/female_base.blend"

    def launch(self):
        if not os.path.exists(self.blender_path):
            print("[Blender] Blender nicht gefunden!")
            return
        subprocess.Popen([self.blender_path, self.blend_file])

    def run_script(self, script_name):
        script_path = f"blender_embed/scripts/{script_name}"
        if not os.path.exists(script_path):
            print(f"[Blender] Skript nicht gefunden: {script_path}")
            return
        subprocess.run([
            self.blender_path,
            "--background",
            self.blend_file,
            "--python", script_path
        ])
