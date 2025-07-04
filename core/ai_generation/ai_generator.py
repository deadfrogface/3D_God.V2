from core.logger import log
from core.ai_generation.fauxpilot_handler import FauxPilotHandler
from core.ai_generation.triposr_handler import TripoSRHandler
from core.ai_generation.charmorph_handler import CharMorphHandler
from core.character_system.character_system import CharacterSystem

class AIGenerator:
    def __init__(self):
        log.info("[AI][AIGenerator.__init__] ▶️ Initialisiere AI-Komponenten...")
        self.fauxpilot = FauxPilotHandler()
        self.triposr = TripoSRHandler()
        self.charmorph = CharMorphHandler()
        self.character_system = CharacterSystem()
        log.success("[AI][AIGenerator.__init__] ✅ Initialisierung abgeschlossen")

    def generate_code(self, prompt):
        log.info(f"[AI][AIGenerator.generate_code] ▶️ Prompt: {prompt}")
        result = self.fauxpilot.generate(prompt)
        log.success("[AI][AIGenerator.generate_code] ✅ Code generiert")
        return result

    def set_image_path(self, path):
        log.info(f"[AI][AIGenerator.set_image_path] ▶️ Bildpfad gesetzt: {path}")
        self.triposr.set_input_image(path)

    def generate_mesh_from_image(self):
        log.info("[AI][AIGenerator.generate_mesh_from_image] ▶️ Starte Mesh-Generierung")
        self.triposr.generate_mesh()
        log.success("[AI][AIGenerator.generate_mesh_from_image] ✅ Mesh-Vorgang abgeschlossen")

    def generate_shape_from_prompt(self, prompt):
        log.info(f"[AI][AIGenerator.generate_shape_from_prompt] ▶️ Prompt: {prompt}")
        result = self.charmorph.generate_shape(prompt)
        if result:
            log.success(f"[AI][AIGenerator.generate_shape_from_prompt] ✅ Ergebnis: {result}")
        else:
            log.error("[AI][AIGenerator.generate_shape_from_prompt] ❌ Kein Ergebnis empfangen")
        return result