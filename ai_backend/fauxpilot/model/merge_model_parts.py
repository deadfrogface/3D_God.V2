import os

def merge_model():
    print("[FauxPilot][merge_model] ▶️ Starte Zusammenführung der Modellteile...")

    parts = [f"pytorch_model.bin.part{i:03d}" for i in range(1, 100) if os.path.exists(f"pytorch_model.bin.part{i:03d}")]
    print(f"[FauxPilot][merge_model] ➕ Gefundene Teile: {len(parts)}")

    if not os.path.exists("pytorch_model.bin") and parts:
        try:
            with open("pytorch_model.bin", "wb") as f_out:
                for part in parts:
                    print(f"[FauxPilot][merge_model] 📦 Füge hinzu: {part}")
                    with open(part, "rb") as f_in:
                        f_out.write(f_in.read())
            print("[FauxPilot][merge_model] ✅ Modell erfolgreich zusammengesetzt → pytorch_model.bin")
        except Exception as e:
            print(f"[FauxPilot][merge_model] ❌ Fehler beim Zusammenführen: {e}")
    else:
        print("[FauxPilot][merge_model] ⚠️ Keine Aktion – Modell existiert bereits oder keine Teile gefunden.")

if __name__ == "__main__":
    merge_model()