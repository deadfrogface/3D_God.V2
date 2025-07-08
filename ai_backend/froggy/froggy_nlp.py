# ai_backend/froggy/froggy_nlp.py

from .froggy_handler import (
    ask_froggy_anything,
    suggest_fix,
    confirm_and_execute_fix,
    give_froggy_feedback,
)
from .froggy_worldview import scan_worldview
from .code_inspector import inspect_all_code
from .fix_generator import apply_fix_to_file
from .connection_inspector import run_connection_inspector
from .froggy_llm import generate_response


def process_natural_input(user_input: str, log_text: str) -> str:
    lower = user_input.lower().strip()

    # 🔍 Loganalyse durch Froggy
    if any(kw in lower for kw in ["analyse", "problem", "was ist los", "fehler"]):
        result = ask_froggy_anything(log_text)
        return f"""❌ Problem: {result.get('problem')}
📎 Ursache: {result.get('cause')}
💡 Vorschlag: {result.get('suggestion')}"""

    # 🔧 Code-Struktur-Fixes
    if "fix" in lower or "reparier" in lower:
        if "code" in lower or "funktion" in lower:
            problems = inspect_all_code()
            if not problems:
                return "✅ Keine strukturellen Codeprobleme gefunden."
            messages = []
            for p in problems:
                messages.append(
                    f"""📂 Datei: {p['file']}
🔍 Problem: {p.get('type', p.get('error', 'Unbekannt'))}
📍 Zeile: {p.get('lineno', '?')}
💡 Fix-Vorschlag: {p.get('fix', '[kein Fix bekannt]')}"""
                )
            return "\n\n".join(messages)
        else:
            fix = suggest_fix(log_text)
            return confirm_and_execute_fix(fix)

    # 🔗 Verbindungsprüfung (z. B. Buttons, Assets)
    if any(kw in lower for kw in ["verbindung", "verbinde", "check verbindung", "connect"]):
        result = run_connection_inspector()
        unused = result.get("unused", [])
        unused_assets = result.get("assets", [])
        unused_ui = result.get("ui", [])

        msg = ""
        if unused:
            msg += f"🔍 Nicht verwendete Funktionen:\n- " + "\n- ".join(unused) + "\n"
        if unused_ui:
            msg += f"\n🔗 Nicht verbundene UI-Elemente:\n- " + "\n- ".join(unused_ui) + "\n"
        if unused_assets:
            msg += f"\n🧱 Unverwendete Assets:\n- " + "\n- ".join(unused_assets)
        return msg if msg else "✅ Alle Verbindungen scheinen korrekt."

    # 🧠 Freie LLM-Anfrage (z. B. Code generieren)
    if any(kw in lower for kw in ["klasse", "panel", "funktion", "code schreiben", "bau", "erzeuge", "methode"]):
        return f"🧠 Froggy generiert:\n\n{generate_response(user_input)}"

    # 📤 Feedback
    if "feedback" in lower and "ok" in lower:
        give_froggy_feedback(log_text, correct_label=0)
        return "✅ Danke! Froggy hat gelernt, dass das die richtige Lösung war."

    # 📦 Modulübersicht
    if "was fehlt" in lower or "module" in lower or "systemstatus" in lower:
        view = scan_worldview()
        missing = view.get("missing", [])
        found = view.get("modules", {})
        return f"""📦 Froggys Systemstatus:
Fehlende Module: {', '.join(missing) if missing else 'Keine'}
Aktive Module: {', '.join(k for k, v in found.items() if v)}"""

    return "🤷‍♂️ Froggy weiß (noch) nicht, wie er darauf reagieren soll."