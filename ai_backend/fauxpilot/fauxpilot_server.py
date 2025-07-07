# ai_backend/fauxpilot/fauxpilot_server.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify

# ⚠️ Modellname hier ggf. anpassen
MODEL_NAME = "Salesforce/codegen-350M-mono"

print("📦 Lade Modell:", MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.eval()
if torch.cuda.is_available():
    model = model.to("cuda")

app = Flask(__name__)

@app.route("/completion", methods=["POST"])
def completion():
    data = request.get_json()
    prompt = data.get("prompt", "")

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        input_ids = input_ids.to("cuda")

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_length=256,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    response = completion[len(prompt):].strip()
    return jsonify({"completion": response})

if __name__ == "__main__":
    print("🚀 FauxPilot Server läuft auf http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
