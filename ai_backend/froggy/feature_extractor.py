import re
import os
import ast


def extract_features(log_text: str) -> list:
    lines = log_text.lower().split("\n")
    return [
        len([l for l in lines if "error" in l]),
        len([l for l in lines if "warning" in l]),
        sum("function" in l for l in lines),
        sum("missing" in l or "not found" in l for l in lines),
        sum("traceback" in l for l in lines),
        sum("fix" in l or "resolve" in l for l in lines),
        int(bool(re.search(r"line \\d+", log_text)))
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
        "inconsistent_classes": 0,
        "ui_parse_failures": 0,
        "missing_ui_signals": 0,
        "unused_slots": 0,
        "duplicate_panels": 0,
        "wrong_paths": 0
    }

    ui_classes = set()
    loaded_panels = {}

    for subdir, _, files in os.walk(root):
        for file in files:
            full_path = os.path.join(subdir, file)
            rel_path = os.path.relpath(full_path, root)

            if file.endswith(".py"):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    tree = ast.parse(code, filename=full_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if not node.body:
                                signals["empty_functions"] += 1
                        elif isinstance(node, ast.ClassDef):
                            if not node.body:
                                signals["inconsistent_classes"] += 1
                            if "Panel" in node.name:
                                panel_name = node.name
                                loaded_panels[panel_name] = loaded_panels.get(panel_name, 0) + 1
                        elif isinstance(node, ast.ImportFrom) and node.module and node.names:
                            if "ui" in node.module and any("signal" in n.name for n in node.names):
                                ui_classes.add(node.module)
                except Exception:
                    signals["broken_imports"] += 1

            if file.endswith(".glb") and "assets" in full_path:
                continue
            if file.endswith(".json") and "config" in full_path:
                continue
            if ".glb" in file.lower() and not os.path.exists(full_path):
                signals["glb_missing"] += 1

            if "blender" in full_path.lower():
                signals["blender_refs"] += 1

            if "ai_backend" in full_path.lower():
                signals["ai_modules"] += 1

            if "\\" in rel_path or "/" in rel_path:
                if not os.path.exists(full_path):
                    signals["wrong_paths"] += 1

    for panel_name, count in loaded_panels.items():
        if count > 1:
            signals["duplicate_panels"] += 1

    return [
        signals["missing_methods"],
        signals["empty_functions"],
        signals["broken_imports"],
        signals["glb_missing"],
        signals["blender_refs"],
        signals["ai_modules"],
        signals["inconsistent_classes"],
        signals["ui_parse_failures"],
        signals["missing_ui_signals"],
        signals["unused_slots"],
        signals["duplicate_panels"],
        signals["wrong_paths"]
    ]
