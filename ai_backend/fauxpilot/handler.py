# ai_backend/fauxpilot/handler.py
import requests

class FauxPilotHandler:
    def __init__(self, host="http://localhost:5000"):
        self.url = f"{host}/v1/engines/codegen/completions"

    def complete(self, prompt: str, max_tokens=128) -> str:
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "stop": ["\n\n"]
        }
        try:
            response = requests.post(self.url, json=payload)
            result = response.json()
            return result.get("choices", [{}])[0].get("text", "").strip()
        except Exception as e:
            return f"[Fehler bei FauxPilot]: {str(e)}"