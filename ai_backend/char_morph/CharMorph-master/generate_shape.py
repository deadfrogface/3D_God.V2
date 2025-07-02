import argparse
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, required=True)
args = parser.parse_args()

prompt = args.prompt.lower()

# Beispielhafte Logik (normalerweise GAN / LoRA)
if "slim" in prompt:
    height = 80
    breast = 20
elif "muscular" in prompt:
    height = 60
    breast = 90
else:
    height = 50
    breast = 50

# Zufallswerte für andere Proportionen
output = {
    "height": height,
    "breast_size": breast,
    "hip_width": random.randint(30, 70),
    "arm_length": random.randint(30, 70),
    "leg_length": random.randint(30, 70)
}

with open("CharMorph-master/output_shape.json", "w") as f:
    json.dump(output, f, indent=4)

print("[CharMorph] Shape erzeugt.")