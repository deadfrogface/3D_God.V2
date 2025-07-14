# core/ai_generation/ai_generator.py

from core.logger import log
from core.ai_generation.fauxpilot_handler import FauxPilotHandler
from core.ai_generation.triposr_handler import TripoSRHandler
from core.ai_generation.charmorph_handler import CharMorphHandler


class AIGenerator:
    def __init__(self, character_system=None):
        log.info("[AI][AIGenerator.__init__] ▶️ Initialisiere AI-Komponenten...")
        self.character_system = character_system  # wird von außen übergeben
        self.fauxpilot = FauxPilotHandler()
        self.triposr = TripoSRHandler()
        self.charmorph = CharMorphHandler()
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
        result_path = self.triposr.generate_mesh()
        if result_path:
            log.success(f"[AI][AIGenerator.generate_mesh_from_image] ✅ Ergebnis: {result_path}")
            if self.character_system and self.character_system.viewport_ref:
                self.character_system.viewport_ref.load_preview(result_path)
        else:
            log.error("[AI][AIGenerator.generate_mesh_from_image] ❌ Kein Mesh erzeugt")
        return result_path

    def generate_shape_from_prompt(self, prompt):
        log.info(f"[AI][AIGenerator.generate_shape_from_prompt] ▶️ Prompt: {prompt}")
        result = self.charmorph.generate_shape(prompt)
        if result:
            log.success(f"[AI][AIGenerator.generate_shape_from_prompt] ✅ Ergebnis: {result}")
            if self.character_system:
                self.character_system.sculpt_data.update(result)
                self.character_system.apply_loaded_state()
        else:
            log.error("[AI][AIGenerator.generate_shape_from_prompt] ❌ Kein Ergebnis empfangen")
        return result

    def generate_full_character(self, prompt: str):
        log.info(f"[AI][AIGenerator.generate_full_character] ▶️ Prompt: {prompt}")
        shape = self.charmorph.generate_shape(prompt)
        mesh = self.triposr.generate_mesh()

        if shape:
            log.success("[AI][AIGenerator.generate_full_character] ✅ Körperform generiert")
            if self.character_system:
                self.character_system.sculpt_data.update(shape)
                self.character_system.apply_loaded_state()
        else:
            log.warning("[AI][AIGenerator.generate_full_character] ⚠️ Keine Körperformdaten erhalten")

        if mesh:
            log.success("[AI][AIGenerator.generate_full_character] ✅ Mesh generiert")
            if self.character_system and self.character_system.viewport_ref:
                self.character_system.viewport_ref.load_preview(mesh)
        else:
            log.error("[AI][AIGenerator.generate_full_character] ❌ Kein Mesh generiert")

        return shape, mesh

    def generate_asset(self, prompt: str):
        log.info(f"[AI][AIGenerator.generate_asset] ▶️ Prompt: {prompt}")
        asset_path = self.triposr.generate_mesh()
        if asset_path and self.character_system:
            self.character_system.add_asset("clothes", asset_path)
            log.success(f"[AI][AIGenerator.generate_asset] ✅ Asset hinzugefügt: {asset_path}")
        else:
            log.error("[AI][AIGenerator.generate_asset] ❌ Kein Asset erzeugt")
        return asset_path
