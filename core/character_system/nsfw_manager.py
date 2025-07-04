from core.logger import log

class NSFWManager:
    def __init__(self):
        log.info("[NSFWManager][__init__] ▶️ Eingabe: (kein Argument)")
        self.nsfw_visible = True  # Standard: sichtbar
        log.success(f"[NSFWManager][__init__] ✅ Standardwert gesetzt: nsfw_visible = {self.nsfw_visible}")

    def toggle_nsfw(self, state: bool):
        log.info(f"[NSFWManager][toggle_nsfw] ▶️ Eingabe: state = {state}")
        self.nsfw_visible = state
        log.success(f"[NSFWManager][toggle_nsfw] ✅ Sichtbarkeit geändert: nsfw_visible = {self.nsfw_visible}")

    def is_visible(self):
        log.info("[NSFWManager][is_visible] ▶️ Eingabe: (kein Argument)")
        log.success(f"[NSFWManager][is_visible] ✅ Rückgabe: {self.nsfw_visible}")
        return self.nsfw_visible