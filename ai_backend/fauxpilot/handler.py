# ai_backend/fauxpilot/handler.py

import os
from ai_backend.fauxpilot.codegen_model import CodegenModel

class FauxPilotHandler:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "model")
        self.model = CodegenModel(model_path)

    def complete(self, prompt: str, max_tokens: int = 128) -> str:
        return self.model.generate(prompt, max_tokens)