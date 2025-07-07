import os

def apply_fix_to_file(file_path: str, lineno: int, fix_code: str) -> str:
    """
    Setzt eine Codezeile ab Zeile `lineno` in die Datei ein.
    Gibt Ergebnis-Text zurück.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Index berechnen (Zeilen zählen bei 1)
        index = lineno - 1
        if index < 0 or index > len(lines):
            return f"❌ Ungültige Zeile {lineno} in Datei {file_path}"

        # Codezeilen vorbereiten
        fix_lines = fix_code.strip().split("\n")
        fix_lines = [line + "\n" for line in fix_lines]

        # Einfügen vor oder überschreibend
        lines[index:index+1] = fix_lines

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return f"✅ Fix eingefügt in {file_path} bei Zeile {lineno}"
    except Exception as e:
        return f"❌ Fehler beim Schreiben: {e}"
