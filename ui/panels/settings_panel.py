from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton
from core.character_system.character_system import CharacterSystem
from ui.style_manager import StyleManager

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        self.config = self.character_system.config
        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙️ Globale Einstellungen"))

        # Theme
        self.theme_toggle = QCheckBox("🌙 Dunkles Theme aktivieren")
        self.theme_toggle.setChecked(self.config.get("theme", "dark") == "dark")
        layout.addWidget(self.theme_toggle)

        # NSFW
        self.nsfw_toggle = QCheckBox("🔞 NSFW-Inhalte anzeigen")
        self.nsfw_toggle.setChecked(self.config.get("nsfw_enabled", True))
        layout.addWidget(self.nsfw_toggle)

        # Controller
        self.controller_toggle = QCheckBox("🎮 Controller-Unterstützung aktivieren")
        self.controller_toggle.setChecked(self.config.get("controller_enabled", True))
        layout.addWidget(self.controller_toggle)

        # Debug
        self.debug_toggle = QCheckBox("🛠 Debug-Konsole anzeigen")
        self.debug_toggle.setChecked(self.config.get("debug_enabled", True))
        layout.addWidget(self.debug_toggle)

        # Anwenden-Button
        btn_apply = QPushButton("💾 Anwenden & Speichern")
        btn_apply.clicked.connect(self.apply_settings)
        layout.addWidget(btn_apply)

        self.setLayout(layout)

    def apply_settings(self):
        self.config["theme"] = "dark" if self.theme_toggle.isChecked() else "light"
        self.config["nsfw_enabled"] = self.nsfw_toggle.isChecked()
        self.config["controller_enabled"] = self.controller_toggle.isChecked()
        self.config["debug_enabled"] = self.debug_toggle.isChecked()
        self.character_system.save_config()

        StyleManager.apply_theme(self.config["theme"])
        print("[Settings] Neue Konfiguration gespeichert:", self.config)