import os
from core.logger import log

def merge_model():
    log.info("[FauxPilot][merge_model] ▶️ Starte Zusammenführung der Modellteile...")

    parts = [f"pytorch_model.bin.part{i:03d}" for i in range(1, 100) if os.path.exists(f"pytorch_model.bin.part{i:03d}")]
    log.info(f"[FauxPilot][merge_model] ➕ Gefundene Teile: {len(parts)}")

    if not os.path.exists("pytorch_model.bin") and parts:
        try:
            with open("pytorch_model.bin", "wb") as f_out:
                for part in parts:
                    log.info(f"[FauxPilot][merge_model] 📦 Füge hinzu: {part}")
                    with open(part, "rb") as f_in:
                        f_out.write(f_in.read())
            log.success("[FauxPilot][merge_model] ✅ Modell erfolgreich zusammengesetzt → pytorch_model.bin")
        except Exception as e:
            log.error(f"[FauxPilot][merge_model] ❌ Fehler beim Zusammenführen: {e}")
    else:
        log.warning("[FauxPilot][merge_model] ⚠️ Keine Aktion – Modell existiert bereits oder keine Teile gefunden.")

if __name__ == "__main__":
    merge_model()