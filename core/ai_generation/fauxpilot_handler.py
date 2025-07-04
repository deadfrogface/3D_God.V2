from core.logger import log

class FauxPilotHandler:
    def generate(self, prompt):
        log.info(f"[AI][FauxPilotHandler.generate] ▶️ Eingabe: {prompt}")
        try:
            code = f"# Blender-Skript-Stub für: {prompt}\nprint('FauxPilot sagt hallo.')"
            log.success("[AI][FauxPilotHandler.generate] ✅ Erfolg: Code erzeugt")
            return code
        except Exception as e:
            log.error(f"[AI][FauxPilotHandler.generate] ❌ Fehler: {e}")
            return None