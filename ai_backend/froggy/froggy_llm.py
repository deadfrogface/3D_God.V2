from transformers import AutoModelForCausalLM, AutoTokenizer import torch import os

📦 Modellname (lokal oder aus HuggingFace, z. B. TinyCoder oder Phi-2)

LLM_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # alternativ: "tiiuae/falcon-rw-1b" oder "microsoft/phi-2"

📁 Cache-Verzeichnis, um HuggingFace-Downloads zu speichern

HF_CACHE = os.path.expanduser("~/.cache/huggingface")

🔄 Gerät auswählen (GPU/CPU)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"🧠 Lade LLM: {LLM_NAME} auf {device}...") tokenizer = AutoTokenizer.from_pretrained(LLM_NAME, cache_dir=HF_CACHE) model = AutoModelForCausalLM.from_pretrained(LLM_NAME, cache_dir=HF_CACHE).to(device) model.eval()

def generate_response(prompt: str, max_tokens: int = 200) -> str: input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device) with torch.no_grad(): output = model.generate( input_ids, max_length=input_ids.shape[1] + max_tokens, do_sample=True, temperature=0.7, top_k=50, top_p=0.95, pad_token_id=tokenizer.eos_token_id ) decoded = tokenizer.decode(output[0], skip_special_tokens=True) return decoded[len(prompt):].strip()

if name == "main": test = "Schreibe eine Python-Klasse namens CharacterPanel mit einer Methode export_character()" print("\n🧪 Test-Prompt:") print(test) print("\n📤 Antwort:") print(generate_response(test))

