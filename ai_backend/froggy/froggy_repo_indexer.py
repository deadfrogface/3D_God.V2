import os
import ast
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
CACHE_PATH = os.path.join(os.path.dirname(__file__), "froggy_project_cache.json")


def is_valid_file(file_path: str) -> bool:
    return file_path.endswith(".py") and "pycache" not in file_path


def scan_python_file(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception as e:
        return {"error": str(e), "path": file_path}

    file_info = {"classes": [], "functions": [], "imports": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            file_info["classes"].append(node.name)
        elif isinstance(node, ast.FunctionDef):
            file_info["functions"].append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                file_info["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                file_info["imports"].append(f"{mod}.{alias.name}")
    return file_info


def scan_project(root: str) -> dict:
    project_data = {}
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if is_valid_file(filename):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, root)
                project_data[rel_path] = scan_python_file(full_path)
    return project_data


def save_cache(data: dict) -> None:
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Projektstruktur gespeichert unter: {CACHE_PATH}")


if __name__ == "__main__":
    print(f"🔍 Scanne Projekt unter: {PROJECT_ROOT}")
    data = scan_project(PROJECT_ROOT)
    save_cache(data)
