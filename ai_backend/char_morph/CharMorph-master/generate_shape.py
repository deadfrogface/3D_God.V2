import argparse
import json
import random

print("[CharMorph][generate_shape] ▶️ Starte Shape-Generierung...")

parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str, nargs="?", default="")
args = parser.parse_args()

prompt = args.prompt.lower()
print(f"[CharMorph][generate_shape] ▶️ Prompt erhalten: '{prompt}'")

# Beispielhafte Logik (normalerweise GAN / LoRA)
if "slim" in prompt:
    height = 80
    breast = 20
    print("[CharMorph][generate_shape] 📏 Detektiert: slim → Höhe 80, Brust 20")
elif "muscular" in prompt:
    height = 60
    breast = 90
    print("[CharMorph][generate_shape] 💪 Detektiert: muscular → Höhe 60, Brust 90")
else:
    height = 50
    breast = 50
    print("[CharMorph][generate_shape] ⚖️ Kein Match → Standardwerte")

# Zufallswerte für andere Proportionen
output = {
    "height": height,
    "breast_size": breast,
    "hip_width": random.randint(30, 70),
    "arm_length": random.randint(30, 70),
    "leg_length": random.randint(30, 70)
}

print(f"[CharMorph][generate_shape] ✅ Ausgabe-Daten: {output}")

# Speichern (optional)
output_path = "CharMorph-master/output_shape.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=4)

print(f"[CharMorph][generate_shape] 💾 Daten gespeichert unter: {output_path}")

# WICHTIG: Als Rückgabe für Python-Bridge
print(json.dumps(output))