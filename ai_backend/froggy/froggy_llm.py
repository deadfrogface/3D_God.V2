# ai_backend/froggy/froggy_llm.py

from core.logger import log

try:
    from ai_backend.fauxpilot.fauxpilot_handler import generate_code  # dein LLM-Modul
except ImportError:
    generate_code = None


def generate_response(prompt: str) -> str:
    """Erzeuge LLM-Antwort aus Benutzereingabe."""
    if not generate_code:
        return "[LLM] ❌ Kein LLM-Modul gefunden (fauxpilot_handler)"
    try:
        result = generate_code(prompt)
        return result.strip() if result else "[LLM] ⚠️ Keine Antwort erhalten"
    except Exception as e:
        log.error(f"[froggy_llm][generate_response] ❌ Fehler: {e}")
        return "[LLM] ❌ Fehler beim Generieren"


def generate_explanation(fix: dict) -> str:
    """Erkläre, warum ein Fehler auftritt, und wie er behoben wird."""
    if not generate_code:
        return "[LLM] ❌ Kein LLM-Modul gefunden (fauxpilot_handler)"

    try:
        prompt = f"""Erkläre das folgende Problem im Code für einen Entwickler:

Problem: {fix.get("problem")}
Ursache: {fix.get("cause")}
Vorschlag: {fix.get("suggestion")}

Bitte gib eine kurze, präzise Erklärung mit Beispielen, wenn sinnvoll."""
        result = generate_code(prompt)
        return result.strip() if result else "[LLM] ⚠️ Keine Erklärung erhalten"
    except Exception as e:
        log.error(f"[froggy_llm][generate_explanation] ❌ Fehler: {e}")
        return "[LLM] ❌ Fehler beim Erklären"
