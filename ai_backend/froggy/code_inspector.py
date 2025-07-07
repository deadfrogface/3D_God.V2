import ast
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def scan_python_files():
    py_files = []
    for root, _, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                py_files.append(full_path)
    return py_files

def inspect_file(path: str) -> list:
    """Analysiert eine Python-Datei und gibt Problemliste zurück"""
    problems = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
    except Exception as e:
        problems.append({
            "file": path,
            "error": f"❌ Kann Datei nicht parsen: {e}"
        })
        return problems

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.body or isinstance(node.body[0], ast.Pass):
                problems.append({
                    "file": path,
                    "type": "leere funktion",
                    "name": node.name,
                    "lineno": node.lineno,
                    "fix": f"def {node.name}(...):\n    # TODO: Implementieren"
                })
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "connect":
                if not node.args:
                    problems.append({
                        "file": path,
                        "type": "Signalbindung ohne Ziel",
                        "lineno": node.lineno,
                        "fix": "# connect(...) → Ziel fehlt"
                    })
    return problems

def inspect_all_code():
    all_problems = []
    for path in scan_python_files():
        result = inspect_file(path)
        if result:
            all_problems.extend(result)
    return all_problems
