# ai_backend/fauxpilot/run_local.py

from handler import FauxPilotHandler
from core.logger import log

def main():
    prompt = "def say_hello():\n    "
    log.info("[FauxPilot][run_local] ▶️ Prompt empfangen:")
    log.info(prompt)

    handler = FauxPilotHandler()
    result = handler.complete(prompt)

    if result:
        log.success("[FauxPilot][run_local] ✅ Antwort erhalten:")
        log.info(result)
    else:
        log.error("[FauxPilot][run_local] ❌ Keine Antwort generiert.")

if __name__ == "__main__":
    main()