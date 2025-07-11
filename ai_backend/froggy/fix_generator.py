import os
import ast
import traceback


def apply_fix_to_file(file_path: str, lineno: int, fix_code: str) -> str:
    """
    Setzt eine Codezeile ab Zeile `lineno` in die Datei ein.
    Gibt Ergebnis-Text zurück.
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Datei nicht gefunden: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lineno < 1 or lineno > len(lines):
            return f"❌ Ungültige Zeile {lineno} in Datei {file_path} (max = {len(lines)})"

        fix_lines = [line + "\n" for line in fix_code.strip().split("\n")]
        index = lineno - 1
        lines[index:index+1] = fix_lines

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return f"✅ Fix eingefügt in {file_path} bei Zeile {lineno}"
    except Exception as e:
        return f"❌ Fehler beim Patchen: {e}"


def is_function_empty(file_path: str, function_name: str) -> bool:
    """
    Prüft, ob eine Funktion leer ist (nur 'pass' oder kein Body).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                if len(node.body) == 0:
                    return True
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    return True
        return False
    except Exception:
        return False


def insert_missing_function_body(file_path: str, function_name: str, body_code: str) -> str:
    """
    Sucht leere Funktion und fügt body_code ein.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith("def ") and function_name in line:
                # nächstes pass oder leeres Block erkennen
                indent = len(line) - len(line.lstrip()) + 4
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == "pass" or lines[j].strip() == "":
                        lines[j] = (" " * indent) + body_code.strip() + "\n"
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        return f"✅ Body in Funktion '{function_name}' eingefügt in {file_path}"
                return f"❌ Keine leere Stelle in Funktion '{function_name}' gefunden"

        return f"❌ Funktion '{function_name}' nicht gefunden"
    except Exception as e:
        return f"❌ Fehler beim Einfügen: {e}\n{traceback.format_exc()}"


def insert_import_if_missing(file_path: str, import_line: str) -> str:
    """
    Fügt einen Import am Anfang der Datei ein, falls nicht vorhanden.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if any(import_line in line for line in lines):
            return f"ℹ️ Import bereits vorhanden in {file_path}"

        # nach letzten Import suchen
        last_import_index = 0
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                last_import_index = i

        lines.insert(last_import_index + 1, import_line + "\n")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return f"✅ Import '{import_line}' hinzugefügt in {file_path}"
    except Exception as e:
        return f"❌ Fehler beim Hinzufügen von Import: {e}"
