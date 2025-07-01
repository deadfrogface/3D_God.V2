class FauxPilotHandler:
    def generate(self, prompt):
        print("[FauxPilot] Empfange Prompt:", prompt)
        return f"# Blender-Skript-Stub für: {prompt}\nprint('FauxPilot sagt hallo.')"