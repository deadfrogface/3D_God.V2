# ai_backend/fauxpilot/run_local.py
from handler import FauxPilotHandler

if __name__ == "__main__":
    prompt = "def hello_world():\n    "
    handler = FauxPilotHandler()
    result = handler.complete(prompt)
    print("🔁 Prompt:\n", prompt)
    print("✅ Ergebnis:\n", result)