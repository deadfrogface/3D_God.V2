from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox
from PySide6.QtCore import Qt
import json

class SettingsPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("⚙️ Einstellungen")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Theme-Auswahl
        theme_label = QLabel("🎨 Theme")
        layout.addWidget(theme_label)
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Hell", "Dunkel", "Cyberpunk"])
        self.theme_box.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_box)

        # NSFW-Modus
        self.nsfw_checkbox = QCheckBox("🔞 NSFW-Modus aktivieren")
        self.nsfw_checkbox.setChecked(self.character_system.nsfw_enabled)
        self.nsfw_checkbox.stateChanged.connect(self.toggle_nsfw)
        layout.addWidget(self.nsfw_checkbox)

        # Controller
        self.controller_checkbox = QCheckBox("🎮 Controller aktivieren")
        self.controller_checkbox.setChecked(self.character_system.controller_enabled)
        self.controller_checkbox.stateChanged.connect(self.toggle_controller)
        layout.addWidget(self.controller_checkbox)

        layout.addStretch()
        self.setLayout(layout)

    def change_theme(self, theme):
        print(f"🎨 Theme gesetzt: {theme}")
        self.character_system.config_data["theme"] = theme
        self.character_system.save_config()

    def toggle_nsfw(self, state):
        enabled = (state == Qt.Checked)
        self.character_system.set_nsfw_mode(enabled)
        self.character_system.config_data["nsfw"] = enabled
        self.character_system.save_config()

    def toggle_controller(self, state):
        enabled = (state == Qt.Checked)
        self.character_system.controller_enabled = enabled
        self.character_system.config_data["controller"] = enabled
        self.character_system.save_config()