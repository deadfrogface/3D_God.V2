# ai_backend/fauxpilot/run_local.py

from handler import FauxPilotHandler

if __name__ == "__main__":
    handler = FauxPilotHandler()
    prompt = "def say_hello():\n    "
    result = handler.complete(prompt)
    print(f"Prompt:\n{prompt}")
    print(f"\nAntwort:\n{result}")