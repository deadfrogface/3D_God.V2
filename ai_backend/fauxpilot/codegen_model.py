# ai_backend/fauxpilot/codegen_model.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class CodegenModel:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.model.eval()

    def generate(self, prompt, max_tokens=128):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"], max_new_tokens=max_tokens, pad_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()