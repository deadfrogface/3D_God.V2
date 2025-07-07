# ai_backend/froggy/froggy_nlp.py

from .froggy_handler import (
    ask_froggy_anything,
    suggest_fix,
    confirm_and_execute_fix,
    give_froggy_feedback
)
from .froggy_worldview import scan_worldview

def process_natural_input(user_input: str, log_text: str) -> str:
    lower = user_input.lower()

    # Analyse starten
    if "analyse" in lower or "problem" in lower or "was ist los" in lower:
        result = ask_froggy_anything(log_text)
        return f"""❌ Problem: {result.get("problem")}
📎 Ursache: {result.get("cause")}
💡 Vorschlag: {result.get("suggestion")}"""

    # Vorschlag mit Bestätigung
    if "fix" in lower or "reparier" in lower or "mach" in lower:
        fix = suggest_fix(log_text)
        return confirm_and_execute_fix(fix)

    # Feedback geben
    if "feedback" in lower and "ok" in lower:
        give_froggy_feedback(log_text, correct_label=0)
        return "✅ Danke! Froggy hat gelernt, dass das die richtige Lösung war."

    # Modulliste
    if "was fehlt" in lower or "module" in lower:
        view = scan_worldview()
        missing = view.get("missing", [])
        found = view.get("modules", {})
        return f"""📦 Froggys Systemstatus:
Fehlende Module: {', '.join(missing) if missing else 'Keine'}
Aktive Module: {', '.join(k for k,v in found.items() if v)}"""

    return "🤷‍♂️ Froggy weiß (noch) nicht, wie er darauf reagieren soll."
