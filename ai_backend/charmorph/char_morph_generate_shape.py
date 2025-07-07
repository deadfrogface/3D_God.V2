import argparse
import json
import random
import os

def log(msg):
    print(f"[CharMorph] {msg}")

def generate_shape(prompt: str) -> dict:
    prompt = prompt.lower()
    log(f"▶️ Prompt erhalten: '{prompt}'")

    # Beispielhafte Regel-basierte Generierung
    if "slim" in prompt:
        height = 80
        breast = 20
        log("📏 Detektiert: slim → height=80, breast=20")
    elif "muscular" in prompt:
        height = 60
        breast = 90
        log("💪 Detektiert: muscular → height=60, breast=90")
    else:
        height = 50
        breast = 50
        log("⚖️ Kein direkter Match → Standardwerte")

    # Zufallswerte für andere Merkmale
    output = {
        "height": height,
        "breast_size": breast,
        "hip_width": random.randint(30, 70),
        "arm_length": random.randint(30, 70),
        "leg_length": random.randint(30, 70)
    }

    log(f"✅ Generierte Shape-Daten: {output}")
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, nargs="?", default="")
    args = parser.parse_args()

    shape_data = generate_shape(args.prompt)

    # Speichern als JSON (optional)
    output_path = os.path.join(os.path.dirname(__file__), "output_shape.json")
    with open(output_path, "w") as f:
        json.dump(shape_data, f, indent=4)
        log(f"💾 Daten gespeichert unter: {output_path}")

    # Rückgabe an aufrufendes Script
    print(json.dumps(shape_data))
