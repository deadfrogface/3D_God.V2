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