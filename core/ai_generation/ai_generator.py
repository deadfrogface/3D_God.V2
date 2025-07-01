from core.ai_generation.fauxpilot_handler import FauxPilotHandler
from core.ai_generation.triposr_handler import TripoSRHandler
from core.ai_generation.charmorph_handler import CharMorphHandler
from core.character_system.character_system import CharacterSystem

class AIGenerator:
    def __init__(self):
        self.fauxpilot = FauxPilotHandler()
        self.triposr = TripoSRHandler()
        self.charmorph = CharMorphHandler()
        self.character_system = CharacterSystem()

    def generate_code(self, prompt):
        return self.fauxpilot.generate(prompt)

    def set_image_path(self, path):
        self.triposr.set_input_image(path)

    def generate_mesh_from_image(self):
        self.triposr.generate_mesh()

    def generate_shape_from_prompt(self, prompt):
        return self.charmorph.generate_shape(prompt)