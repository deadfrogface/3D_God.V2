import os
import json
import torch
from ai_backend.froggy.froggy_brain import predict, train_feedback, train_on_example
from ai_backend.froggy.froggy_worldview import scan_worldview
from ai_backend.froggy.feature_extractor import extract_features
from ai_backend.froggy.froggy_llm import generate_explanation

# 🔍 Hauptanalyse
def ask_froggy_anything(log_text="") -> dict:
    features = extract_features(log_text)
    prediction = predict(features)
    diagnosis = get_error_description(prediction)
    fix_fn = FIX_FUNCTIONS.get(prediction, None)

    result = {
        "problem": diagnosis.get("problem"),
        "cause": diagnosis.get("cause"),
        "suggestion": diagnosis.get("suggestion"),
        "can_fix": diagnosis.get("can_fix", False),
        "fix_fn": fix_fn,
        "features": features,
        "predicted_label": prediction
    }

    try:
        result["explanation"] = generate_explanation(result)
    except Exception:
        result["explanation"] = "(⚠️ Keine LLM-Erklärung verfügbar)"

    return result

# 🧠 Vorschlag mit Priorisierung & Fix-Vorschau
def suggest_fix(log_text="") -> dict:
    features = extract_features(log_text)
    error_id = predict(features)
    diagnosis = get_error_description(error_id)
    fix_fn = FIX_FUNCTIONS.get(error_id, None)
    worldview = scan_worldview()

    result = {
        "error_id": error_id,
        "problem": diagnosis.get("problem"),
        "cause": diagnosis.get("cause"),
        "suggestion": diagnosis.get("suggestion"),
        "can_fix": diagnosis.get("can_fix", False),
        "priority": diagnosis.get("priority", "mittel"),
        "fix_code": diagnosis.get("fix_code", "[interner Methodenaufruf]"),
        "fix_fn": fix_fn,
        "target_file": diagnosis.get("target_file"),
        "features": features,
        "world_info": worldview
    }

    try:
        result["explanation"] = generate_explanation(result)
    except Exception:
        result["explanation"] = "(⚠️ Keine LLM-Erklärung verfügbar)"

    return result

# ❓ Bestätigung & Ausführung + Autotrain + Fehlerabfang
def confirm_and_execute_fix(fix: dict) -> str:
    if not fix.get("can_fix") or not fix.get("fix_fn"):
        return "❌ Kein automatischer Fix verfügbar."

    print(f"""
🧠 Froggy Vorschlag:
❌ Problem: {fix['problem']}
📎 Ursache: {fix['cause']}
💡 Vorschlag: {fix['suggestion']}
📂 Datei: {fix['target_file']}
📈 Priorität: {fix['priority']}

🛠 Fix-Vorschau:
{fix['fix_code']}

📘 Erklärung:
{fix.get('explanation')}

❓ Jetzt anwenden? (ja/nein)
""")
    confirm = input(">>> ").strip().lower()
    if confirm in ("ja", "yes", "y"):
        try:
            result = fix['fix_fn']()
            features = fix.get("features")
            label = fix.get("error_id")
            if features and label is not None:
                train_on_example(features, label)
            return f"✅ Fix angewendet: {result}"
        except Exception as e:
            return f"❌ Fehler beim Ausführen des Fixes: {e}"
    return "🛑 Fix abgebrochen."

# 🔁 Manuelles Feedback (optional)
def give_froggy_feedback(log_text: str, correct_label: int):
    features = extract_features(log_text)
    train_feedback(features, correct_label)

# 🧠 Fehler-Definitionen laden
def get_error_description(error_id: int) -> dict:
    path = os.path.join(os.path.dirname(__file__), "error_tags.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get(str(error_id), DEFAULT_ERROR)
    return DEFAULT_ERROR

# 🧱 Fallback
DEFAULT_ERROR = {
    "problem": "Unbekannter Fehler im System",
    "cause": "Keine Analyse möglich",
    "suggestion": "Bitte manuell prüfen",
    "can_fix": False
}

# 🛠 Beispielhafte Fix-Funktionen
def fix_triposr_bbox():
    from ai_backend.triposr.triposr_handler import enable_default_bbox
    return enable_default_bbox()

def fix_yolo_confidence():
    from ai_backend.yolov7.yolov7_handler import set_confidence_threshold
    return set_confidence_threshold(0.15)

FIX_FUNCTIONS = {
    1: fix_yolo_confidence,
    2: fix_triposr_bbox
}

# 💬 Erklärung durch LLM (optional direkt nutzbar)
def explain_froggy_diagnosis(fix: dict) -> str:
    try:
        return generate_explanation(fix)
    except Exception as e:
        return f"❌ LLM-Erklärung fehlgeschlagen: {e}"
