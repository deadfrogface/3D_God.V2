import os
import ast

IGNORED_DIRS = {"__pycache__", "venv", ".git", ".idea", "build", "dist"}
PYTHON_EXT = ".py"
ASSET_EXTS = {".glb", ".fbx", ".png", ".jpg", ".jpeg", ".json", ".shader", ".txt", ".cfg"}
ASSET_DIRS = {"assets", "resources", "data", "models"}

def run_connection_inspector() -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    found_functions = set()
    called_functions = set()
    buttons = {}
    connected_buttons = set()
    all_assets = set()
    used_assets = set()
    messages = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter ignorierte Ordner
        if any(ignored in dirpath for ignored in IGNORED_DIRS):
            continue

        # 🧠 Code analysieren
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)

            # ⬛ Python-Dateien analysieren
            if fname.endswith(PYTHON_EXT):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        source = f.read()
                    tree = ast.parse(source)

                    for node in ast.walk(tree):
                        # Funktionen merken
                        if isinstance(node, ast.FunctionDef):
                            found_functions.add((node.name, fpath, node.lineno))
                        # Funktionsaufrufe erkennen
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                            called_functions.add(node.func.id)
                        # UI-Buttons erfassen
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and "btn" in target.id.lower():
                                    buttons[target.id] = (fpath, node.lineno)
                        # Button-Verbindungen
                        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                            func = node.value.func
                            if isinstance(func, ast.Attribute) and "connect" in func.attr:
                                if isinstance(func.value, ast.Attribute) and func.value.attr == "clicked":
                                    if isinstance(func.value.value, ast.Name):
                                        connected_buttons.add(func.value.value.id)
                except Exception as e:
                    messages.append(f"❌ Fehler beim Parsen von {fpath}: {e}")

            # 📂 Assets sammeln
            for ext in ASSET_EXTS:
                if fname.endswith(ext):
                    relpath = os.path.relpath(fpath, root)
                    all_assets.add(relpath.replace("\\", "/"))

            # 🔍 Asset-Verwendung prüfen
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for asset in list(all_assets):
                        if asset in content:
                            used_assets.add(asset)
            except:
                pass

    # 🧩 Unverbundene Funktionen
    unused = [f for f in found_functions if f[0] not in called_functions]
    if unused:
        messages.append("🔍 Nicht verwendete Funktionen:")
        for name, fpath, lineno in unused:
            messages.append(f"- {name} in {os.path.relpath(fpath, root)}:{lineno}")

    # 🔗 Unverbundene Buttons
    disconnected = [b for b in buttons if b not in connected_buttons]
    if disconnected:
        messages.append("🔗 Nicht verbundene UI-Buttons:")
        for b in disconnected:
            fpath, lineno = buttons[b]
            messages.append(f"- {b} in {os.path.relpath(fpath, root)}:{lineno}")

    # 📦 Unverwendete Assets
    missing_assets = all_assets - used_assets
    if missing_assets:
        messages.append("🧱 Unverwendete Assets:")
        for asset in sorted(missing_assets):
            messages.append(f"- {asset} (nicht referenziert im Code)")

    if not messages:
        return "✅ Alle Verbindungen scheinen korrekt zu sein."

    return "\n".join(messages)