from core.ai_generation.fauxpilot_handler import FauxPilotHandler
from core.ai_generation.triposr_handler import TripoSRHandler

class AIGenerator:
    def __init__(self):
        self.fauxpilot = FauxPilotHandler()
        self.triposr = TripoSRHandler()

    def generate_code(self, prompt):
        return self.fauxpilot.generate(prompt)

    def set_image_path(self, path):
        self.triposr.set_input_image(path)

    def generate_mesh_from_image(self):
        self.triposr.generate_mesh()