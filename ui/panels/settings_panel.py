from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox
from core.character_system.character_system import CharacterSystem
from ui.style_manager import StyleManager
import json

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.character_system = CharacterSystem()

        self.theme_label = QLabel("Design-Thema:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)

        self.nsfw_checkbox = QCheckBox("NSFW-Modus aktiviert")
        self.nsfw_checkbox.setChecked(self.character_system.config.get("nsfw_enabled", True))
        self.nsfw_checkbox.stateChanged.connect(self.toggle_nsfw)

        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(self.nsfw_checkbox)
        self.setLayout(layout)

    def change_theme(self, theme_name):
        self.character_system.config["theme"] = theme_name
        StyleManager.apply_theme(theme_name)
        self.character_system.save_config()

    def toggle_nsfw(self, state):
        self.character_system.config["nsfw_enabled"] = state == 2
        self.character_system.save_config()
