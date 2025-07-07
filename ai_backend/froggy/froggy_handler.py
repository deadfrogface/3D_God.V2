# ai_backend/froggy/froggy_handler.py

import os
import json
import torch
from ai_backend.froggy.froggy_brain import predict, train_feedback

# Fehlerklassifikationen + Vorschläge
def ask_froggy_anything(log_text="") -> dict:
    features = extract_log_features(log_text)
    prediction = predict(features)
    diagnosis = get_error_description(prediction)

    fix_fn = FIX_FUNCTIONS.get(prediction, lambda: "Kein Fix verfügbar")

    return {
        "problem": diagnosis.get("problem"),
        "cause": diagnosis.get("cause"),
        "suggestion": diagnosis.get("suggestion"),
        "can_fix": diagnosis.get("can_fix", False),
        "fix_fn": fix_fn,
        "features": features,
        "predicted_label": prediction
    }

# Nutzer gibt Feedback: das war richtig/nicht richtig
def give_froggy_feedback(log_text: str, correct_label: int):
    features = extract_log_features(log_text)
    train_feedback(features, correct_label)

# Dummy-Feature-Vektor aus Logtext
def extract_log_features(log_text: str) -> list:
    lines = log_text.lower().split("\n")
    return [
        sum("error" in l for l in lines),
        sum("warning" in l for l in lines),
        sum("yolo" in l for l in lines),
        sum("triposr" in l for l in lines),
        sum("export" in l for l in lines),
        sum("success" in l for l in lines),
        sum("mesh" in l for l in lines)
    ]

def get_error_description(error_id: int) -> dict:
    path = os.path.join(os.path.dirname(__file__), "error_tags.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get(str(error_id), DEFAULT_ERROR)
    return DEFAULT_ERROR

# Fallback-Beschreibung
DEFAULT_ERROR = {
    "problem": "Unbekannter Fehler im System",
    "cause": "Keine Analyse möglich",
    "suggestion": "Bitte manuell prüfen",
    "can_fix": False
}

# Reparaturfunktionen pro Fehler-ID
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
