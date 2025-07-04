# ai_backend/fauxpilot/codegen_model.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class CodegenModel:
    def __init__(self, model_path):
        print(f"[FauxPilot][CodegenModel.__init__] ▶️ Lade Tokenizer und Modell von: {model_path}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path)
            self.model.eval()
            print("[FauxPilot][CodegenModel.__init__] ✅ Modell erfolgreich geladen")
        except Exception as e:
            print(f"[FauxPilot][CodegenModel.__init__] ❌ Fehler beim Laden: {e}")

    def generate(self, prompt, max_tokens=128):
        print(f"[FauxPilot][CodegenModel.generate] ▶️ Prompt empfangen (max_tokens={max_tokens})")
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"], max_new_tokens=max_tokens, pad_token_id=self.tokenizer.eos_token_id
                )
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
            print("[FauxPilot][CodegenModel.generate] ✅ Generierung abgeschlossen")
            return result
        except Exception as e:
            print(f"[FauxPilot][CodegenModel.generate] ❌ Fehler bei Generierung: {e}")
            return ""