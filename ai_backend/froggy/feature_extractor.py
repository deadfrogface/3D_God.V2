# ai_backend/froggy/feature_extractor.py

import re
import os
import ast


def extract_features(log_text: str) -> list:
    lines = log_text.lower().split("\n")
    return [
        len([l for l in lines if "error" in l]),                               # Fehler
        len([l for l in lines if "warning" in l]),                             # Warnungen
        sum("function" in l for l in lines),                                   # Funktionserwähnungen
        sum("missing" in l or "not found" in l for l in lines),              # Fehlende Dinge
        sum("traceback" in l for l in lines),                                  # Tracebacks
        sum("fix" in l or "resolve" in l for l in lines),                    # Reparaturhinweise
        int(bool(re.search(r"line \\d+", log_text)))                        # Zeilenangabe
    ] + _extract_project_signals()


def _extract_project_signals() -> list:
    """
    Analysiert das Projekt global – z. B. auf fehlende Methoden, Assets, .glb-Dateien, Inkonsistenzen.
    Liefert Zusatz-Features.
    """
    root = os.path.abspath(".")
    signals = {
        "missing_methods": 0,
        "empty_functions": 0,
        "broken_imports": 0,
        "glb_missing": 0,
        "blender_refs": 0,
        "ai_modules": 0,
        "inconsistent_classes": 0
    }

    for subdir, _, files in os.walk(root):
        for file in files:
            full_path = os.path.join(subdir, file)

            if file.endswith(".py"):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    tree = ast.parse(code, filename=full_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and not node.body:
                            signals["empty_functions"] += 1
                        elif isinstance(node, ast.ClassDef) and not node.body:
                            signals["inconsistent_classes"] += 1
                except Exception:
                    signals["broken_imports"] += 1

            if file.endswith(".glb") and "assets" in full_path:
                continue  # okay
            if file.endswith(".json") and "config" in full_path:
                continue
            if ".glb" in file.lower() and not os.path.exists(full_path):
                signals["glb_missing"] += 1

            if "blender" in full_path.lower():
                signals["blender_refs"] += 1

            if "ai_backend" in full_path.lower():
                signals["ai_modules"] += 1

    return [
        signals["missing_methods"],
        signals["empty_functions"],
        signals["broken_imports"],
        signals["glb_missing"],
        signals["blender_refs"],
        signals["ai_modules"],
        signals["inconsistent_classes"]
    ]
