from .froggy_handler import (
    ask_froggy_anything,
    suggest_fix,
    confirm_and_execute_fix,
    give_froggy_feedback,
)
from .froggy_worldview import scan_worldview
from .code_inspector import inspect_all_code
from .fix_generator import apply_fix_to_file
from .froggy_llm import generate_response


def process_natural_input(user_input: str, log_text: str) -> str:
    lower = user_input.lower()

    # Loganalyse durch Modell
    if "analyse" in lower or "problem" in lower or "was ist los" in lower:
        result = ask_froggy_anything(log_text)
        return (
            f"❌ Problem: {result.get('problem')}\n\n"
            f"📎 Ursache: {result.get('cause')}\n"
            f"💡 Vorschlag: {result.get('suggestion')}"
        )

    # NLP-gesteuerter Code-Fix
    if any(kw in lower for kw in ["fix", "reparier", "mach", "autofix"]):
        problems = inspect_all_code()
        if not problems:
            return "✅ Keine strukturellen Codeprobleme gefunden."

        messages = []
        for p in problems:
            message = (
                f"📂 Datei: {p['file']}\n"
                f"🔍 Problem: {p.get('type', p.get('error', 'Unbekannt'))}\n"
                f"📍 Zeile: {p.get('lineno', '?')}\n"
                f"💡 Fix-Vorschlag: {p.get('fix', '[kein Fix bekannt]')}"
            )
            messages.append(message)

            if p.get("autofix", True):
                result = apply_fix_to_file(
                    file_path=p["file"],
                    lineno=p.get("lineno", 0),
                    fix_code=p.get("fix", ""),
                )
                messages.append(f"✅ Automatisch repariert: {result}")
            else:
                confirm = input("🐸 Fix jetzt einfügen? (ja/nein): ").strip().lower()
                if confirm in ("ja", "yes", "y"):
                    result = apply_fix_to_file(
                        file_path=p["file"],
                        lineno=p.get("lineno", 0),
                        fix_code=p.get("fix", ""),
                    )
                    messages.append(f"✅ Ergebnis: {result}")
                else:
                    messages.append("🛑 Übersprungen.")

        return "\n\n".join(messages)

    # Verbindungsprüfung
    if any(kw in lower for kw in ["verbindung", "verbinde", "verknüpfung"]):
        return run_connection_inspector()

    # Freie Codegenerierung durch LLM
    if any(kw in lower for kw in ["klasse", "panel", "methode", "funktion", "code schreiben"]):
        response = generate_response(user_input)
        return f"🧠 Froggy generiert:\n\n{response}"

    # Feedback-Verarbeitung
    if "feedback" in lower and "ok" in lower:
        give_froggy_feedback(log_text, correct_label=0)
        return "✅ Danke! Froggy hat gelernt, dass das die richtige Lösung war."

    # Modulübersicht & Worldview
    if any(kw in lower for kw in ["was fehlt", "module", "systemstatus"]):
        view = scan_worldview()
        missing = view.get("missing", [])
        found = view.get("modules", {})
        return (
            "📦 Froggys Systemstatus:\n\n"
            f"Fehlende Module: {', '.join(missing) if missing else 'Keine'}\n"
            f"Aktive Module: {', '.join(k for k, v in found.items() if v)}"
        )

    # Allgemeiner LLM-Fallback
    return generate_response(user_input)
