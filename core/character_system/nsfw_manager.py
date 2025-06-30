class NSFWManager:
    def __init__(self):
        self.nsfw_visible = True  # Standard: sichtbar

    def toggle_nsfw(self, state: bool):
        self.nsfw_visible = state

    def is_visible(self):
        return self.nsfw_visible
