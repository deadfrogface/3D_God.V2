import os

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