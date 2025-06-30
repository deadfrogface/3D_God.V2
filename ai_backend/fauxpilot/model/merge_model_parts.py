# ai_backend/fauxpilot/model/merge_model_parts.py

import os

def merge_model():
    parts = [f"pytorch_model.bin.part{i}" for i in range(1, 10) if os.path.exists(f"pytorch_model.bin.part{i}")]
    if not os.path.exists("pytorch_model.bin") and parts:
        with open("pytorch_model.bin", "wb") as f_out:
            for part in parts:
                with open(part, "rb") as f_in:
                    f_out.write(f_in.read())
        print("[FauxPilot] Modell zusammengesetzt.")

if __name__ == "__main__":
    merge_model()
