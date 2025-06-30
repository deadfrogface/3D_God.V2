from .nsfw_manager import NSFWManager
from .preset_handler import PresetHandler

class CharacterSystem:
    def __init__(self):
        self.nsfw_manager = NSFWManager()
        self.preset_handler = PresetHandler()
        self.current_data = {
            "name": "Unbenannt",
            "gender": "unknown",
            "race": "human",
            "attributes": {},
            "assets": []
        }

    def set_nsfw_mode(self, enabled: bool):
        self.nsfw_manager.toggle_nsfw(enabled)

    def is_nsfw(self):
        return self.nsfw_manager.is_visible()

    def load_preset(self, name: str):
        data = self.preset_handler.load_preset(name)
        if data:
            self.current_data = data
            return True
        return False

    def save_preset(self, name: str):
        self.preset_handler.save_preset(name, self.current_data)

    def get_current_data(self):
        return self.current_data

    def set_current_data(self, data: dict):
        self.current_data = data
