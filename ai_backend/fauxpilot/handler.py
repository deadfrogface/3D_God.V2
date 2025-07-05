import os
from ai_backend.fauxpilot.codegen_model import CodegenModel
from core.logger import log  # ← Logging einbinden

class FauxPilotHandler:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "model")
        log.info(f"[FauxPilot][Handler.__init__] ▶️ Initialisiere mit Model-Pfad: {model_path}")
        self.model = CodegenModel(model_path)
        log.success("[FauxPilot][Handler.__init__] ✅ Modell geladen")

    def complete(self, prompt: str, max_tokens: int = 128) -> str:
        log.info(f"[FauxPilot][Handler.complete] ▶️ Prompt erhalten (max_tokens={max_tokens}):\n{prompt}")
        try:
            result = self.model.generate(prompt, max_tokens)
            log.success("[FauxPilot][Handler.complete] ✅ Antwort generiert")
            return result
        except Exception as e:
            log.error(f"[FauxPilot][Handler.complete] ❌ Fehler beim Generieren: {e}")
            return ""
