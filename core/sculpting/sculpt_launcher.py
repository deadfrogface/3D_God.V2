import subprocess import os from core.logger import log

SCULPT_SCRIPT = os.path.join("blender_embed", "sculpt_main.py")

class SculptLauncher: def init(self, blender_path="blender"): self.blender_path = blender_path

def launch(self, region="head"):
    if not os.path.exists(SCULPT_SCRIPT):
        log.error(f"[SculptLauncher] ❌ sculpt_main.py nicht gefunden: {SCULPT_SCRIPT}")
        return

    log.info(f"[SculptLauncher] ▶️ Starte Blender mit Fokus auf '{region}'...")
    try:
        subprocess.run([
            self.blender_path,
            "--python", SCULPT_SCRIPT,
            "--", region
        ])
        log.success("[SculptLauncher] ✅ Sculpting abgeschlossen")
    except Exception as e:
        log.error(f"[SculptLauncher] ❌ Fehler beim Start: {e}")

