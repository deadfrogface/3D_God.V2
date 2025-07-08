ai_backend/froggy/connection_inspector.py

import os
import ast

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(file), '../../..'))

IGNORED_DIRS = {"pycache", "venv", ".git", ".idea", "build", "dist"} PYTHON_EXT = ".py" ASSET_EXTS = {".glb", ".fbx", ".png", ".jpg", ".jpeg", ".json", ".shader", ".txt", ".cfg"} ASSET_DIRS = {"assets", "resources", "data", "models"}

def find_python_files(base_path=PROJECT_ROOT): for root, dirs, files in os.walk(base_path): dirs[:] = [d for d in dirs if d not in IGNORED_DIRS] for file in files: if file.endswith(PYTHON_EXT): yield os.path.join(root, file)

def find_asset_files(base_path=PROJECT_ROOT): asset_paths = [] for root, dirs, files in os.walk(base_path): if not any(part in root for part in ASSET_DIRS): continue for file in files: ext = os.path.splitext(file)[1].lower() if ext in ASSET_EXTS: asset_paths.append(os.path.relpath(os.path.join(root, file), base_path)) return asset_paths

def find_used_asset_paths(): used_assets = set() for path in find_python_files(): try: with open(path, encoding="utf-8") as f: content = f.read() for ext in ASSET_EXTS: for line in content.splitlines(): if ext in line: fragments = line.split('"') + line.split("'") for frag in fragments: if ext in frag: used_assets.add(frag.strip()) except Exception: continue return used_assets

def find_defined_but_unused_functions(): defined = set() called = set()

for path in find_python_files():
    try:
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined.add((node.name, path))
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    called.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    called.add(node.func.attr)
    except Exception:
        continue

unused = [(name, path) for (name, path) in defined if name not in called and not name.startswith("_")]
return unused

def find_unlinked_ui_elements(): buttons = [] connections = set()

for path in find_python_files():
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()

        if "QPushButton" not in content:
            continue

        tree = ast.parse(content, filename=path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call) and hasattr(node.value.func, "id"):
                    if node.value.func.id == "QPushButton":
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                buttons.append((target.id, path))

            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                func = node.value.func
                if isinstance(func, ast.Attribute):
                    if func.attr.startswith("connect"):
                        if isinstance(func.value, ast.Attribute):
                            connections.add(func.value.value.id)
                        elif isinstance(func.value, ast.Name):
                            connections.add(func.value.id)
    except Exception:
        continue

unlinked = [(btn, path) for (btn, path) in buttons if btn not in connections]
return unlinked

def find_unlinked_assets(): all_assets = find_asset_files() used = find_used_asset_paths() unused = [a for a in all_assets if not any(u in a for u in used)] return unused

def run_connection_inspector(with_fixes=True): results = [] unused_funcs = find_defined_but_unused_functions() if unused_funcs: results.append("🔍 Nicht verwendete Funktionen:") for name, path in unused_funcs: results.append(f"- {name} in {path}") if with_fixes: results.append(f"  💡 Vorschlag: Funktion '{name}' aufrufen oder entfernen.")

unlinked_btns = find_unlinked_ui_elements()
if unlinked_btns:
    results.append("\n🔗 Nicht verbundene UI-Buttons:")
    for btn, path in unlinked_btns:
        results.append(f"- {btn} in {path}")
        if with_fixes:
            results.append(f"  💡 Vorschlag: {btn}.clicked.connect(...) einfügen.")

unlinked_assets = find_unlinked_assets()
if unlinked_assets:
    results.append("\n🧱 Unverwendete Assets:")
    for a in unlinked_assets:
        results.append(f"- {a}")
        if with_fixes:
            results.append(f"  💡 Vorschlag: Asset laden, z. B. mit `load_asset('{a}')`.")

return "\n".join(results) if results else "✅ Alle Verbindungen sehen gut aus."

if name == "main": print(run_connection_inspector())

