from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox, QPushButton
import json
from pathlib import Path

class SettingsPanel(QWidget):
    def __init__(self, config, callback_reload=None):
        super().__init__()
        self.config = config
        self.callback_reload = callback_reload
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ Einstellungen"))

        # Theme Auswahl
        self.theme_box = QComboBox()
        self.theme_box.addItems(["cyberpunk", "hellboy_dark"])
        self.theme_box.setCurrentText(self.config.get("theme", "cyberpunk"))
        layout.addWidget(QLabel("🎨 Theme:"))
        layout.addWidget(self.theme_box)

        # NSFW-Toggle
        self.nsfw_check = QCheckBox("🔞 NSFW-Modus aktivieren")
        self.nsfw_check.setChecked(self.config.get("nsfw_enabled", True))
        layout.addWidget(self.nsfw_check)

        # Controller-Toggle
        self.ctrl_check = QCheckBox("🎮 PlayStation Controller aktivieren")
        self.ctrl_check.setChecked(self.config.get("controller_enabled", True))
        layout.addWidget(self.ctrl_check)

        # Speichern-Button
        save_btn = QPushButton("💾 Einstellungen speichern")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        layout.addStretch()
        self.setLayout(layout)

    def save_settings(self):
        self.config["theme"] = self.theme_box.currentText()
        self.config["nsfw_enabled"] = self.nsfw_check.isChecked()
        self.config["controller_enabled"] = self.ctrl_check.isChecked()

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

        if self.callback_reload:
            self.callback_reload()