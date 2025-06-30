# ai_backend/fauxpilot/codegen_model.py

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class CodegenModel:
    def __init__(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.float32)
        self.model.eval()

    def complete(self, prompt, max_tokens=128):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            output = self.model.generate(input_ids, max_new_tokens=max_tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True).replace(prompt, "").strip()