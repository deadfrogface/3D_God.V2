# ai_backend/fauxpilot/run_local.py

from handler import FauxPilotHandler

def main():
    prompt = "def say_hello():\n    "
    print("[FauxPilot][run_local] ▶️ Prompt empfangen:")
    print(prompt)

    handler = FauxPilotHandler()
    result = handler.complete(prompt)

    if result:
        print("[FauxPilot][run_local] ✅ Antwort erhalten:")
        print(result)
    else:
        print("[FauxPilot][run_local] ❌ Keine Antwort generiert.")

if __name__ == "__main__":
    main()