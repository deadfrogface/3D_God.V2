ai_backend/froggy/froggy_nlp.py

from .froggy_handler import (
    ask_froggy_anything,
    suggest_fix,
    confirm_and_execute_fix,
    give_froggy_feedback
)

from .froggy_worldview import scan_worldview
from .code_inspector import inspect_all_code
from .fix_generator import apply_fix_to_file
from .connection_inspector import run_connection_inspector

def process_natural_input(user_input: str, log_text: str) -> str: lower = user_input.lower()

# 🔍 Loganalyse
if "analyse" in lower or "problem" in lower or "was ist los" in lower:
    result = ask_froggy_anything(log_text)
    return f"""❌ Problem: {result.get("problem")}

📎 Ursache: {result.get("cause")} 💡 Vorschlag: {result.get("suggestion")}"""

# 🔗 Verbindungsscan
if "verbindung" in lower or "verkn\u00fcpfung" in lower or "knopf tut nichts" in lower or "knopf funktioniert nicht" in lower:
    return run_connection_inspector()

# 🧠 Komplett-Scan + interaktive Reparatur
if "pr\u00fcfe alles" in lower or "check alles" in lower or "alles fixen" in lower:
    result = run_connection_inspector(with_fixes=True)
    return result

# 🧠 NLP-gesteuerter Code-Fix
if "fix" in lower or "reparier" in lower or "mach" in lower:
    if "code" in lower or "funktion" in lower or "leer" in lower:
        problems = inspect_all_code()
        if not problems:
            return "✅ Keine strukturellen Codeprobleme gefunden."

        messages = []
        for p in problems:
            messages.append(f"""📂 Datei: {p['file']}

🔍 Problem: {p.get('type', p.get('error', 'Unbekannt'))} 📍 Zeile: {p.get('lineno', '?')} 💡 Fix-Vorschlag: {p.get('fix', '[kein Fix bekannt]')} """) confirm = input("🐸 Fix jetzt einfügen? (ja/nein): ").strip().lower() if confirm in ("ja", "yes", "y"): result = apply_fix_to_file( file_path=p["file"], lineno=p.get("lineno", 0), fix_code=p.get("fix", "") ) messages.append(f"✅ Ergebnis: {result}") else: messages.append("🛑 Übersprungen.") return "\n".join(messages) else: fix = suggest_fix(log_text) return confirm_and_execute_fix(fix)

# 📤 Feedback
if "feedback" in lower and "ok" in lower:
    give_froggy_feedback(log_text, correct_label=0)
    return "✅ Danke! Froggy hat gelernt, dass das die richtige L\u00f6sung war."

# 🧩 Module & Systemstatus
if "was fehlt" in lower or "module" in lower:
    view = scan_worldview()
    missing = view.get("missing", [])
    found = view.get("modules", {})
    return f"""📦 Froggys Systemstatus:

Fehlende Module: {', '.join(missing) if missing else 'Keine'} Aktive Module: {', '.join(k for k,v in found.items() if v)}"""

# 🧾 Exportprobleme
if "export" in lower and ("geht nicht" in lower or "funktioniert nicht" in lower or "fehlt" in lower or "tut nichts" in lower):
    return run_connection_inspector()

return "🤷‍♂️ Froggy wei\u00df (noch) nicht, wie er darauf reagieren soll."

