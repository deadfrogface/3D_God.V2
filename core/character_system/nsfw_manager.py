class NSFWManager:
    def __init__(self):
        print("[NSFWManager][__init__] ▶️ Eingabe: (kein Argument)")
        self.nsfw_visible = True  # Standard: sichtbar
        print(f"[NSFWManager][__init__] ✅ Standardwert gesetzt: nsfw_visible = {self.nsfw_visible}")

    def toggle_nsfw(self, state: bool):
        print(f"[NSFWManager][toggle_nsfw] ▶️ Eingabe: state = {state}")
        self.nsfw_visible = state
        print(f"[NSFWManager][toggle_nsfw] ✅ Sichtbarkeit geändert: nsfw_visible = {self.nsfw_visible}")

    def is_visible(self):
        print("[NSFWManager][is_visible] ▶️ Eingabe: (kein Argument)")
        print(f"[NSFWManager][is_visible] ✅ Rückgabe: {self.nsfw_visible}")
        return self.nsfw_visible