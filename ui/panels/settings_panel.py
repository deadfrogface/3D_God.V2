from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QComboBox
)
from core.logger import log
from ui.panels.debug_console import DebugConsole

class SettingsPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        log.info("[Settings][__init__] ▶️ Initialisiere SettingsPanel...")

        self.character_system = character_system
        self.debug_console = None
        self.config = self.character_system.config

        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙ Einstellungen"))

        # 🎨 Theme Dropdown
        layout.addWidget(QLabel("🎨 Theme"))
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(["dark", "light", "cyberpunk"])
        self.theme_dropdown.setCurrentText(self.config.get("theme", "dark"))
        self.theme_dropdown.currentTextChanged.connect(self.set_theme)
        layout.addWidget(self.theme_dropdown)

        # 🔞 NSFW Checkbox
        self.nsfw_checkbox = QCheckBox("🔞 NSFW-Modus aktivieren")
        self.nsfw_checkbox.setChecked(self.character_system.nsfw_enabled)
        self.nsfw_checkbox.stateChanged.connect(self.set_nsfw)
        layout.addWidget(self.nsfw_checkbox)

        # 🎮 Controller Checkbox
        self.controller_checkbox = QCheckBox("🎮 Controller-Unterstützung")
        self.controller_checkbox.setChecked(self.config.get("controller_enabled", True))
        self.controller_checkbox.stateChanged.connect(self.set_controller)
        layout.addWidget(self.controller_checkbox)

        # 🐞 Debug-Konsole Button
        btn_debug = QPushButton("🐞 Debug-Konsole anzeigen")
        btn_debug.clicked.connect(self.toggle_debug_console)
        layout.addWidget(btn_debug)

        self.setLayout(layout)
        log.info("[Settings][__init__] ✅ Panel initialisiert.")

    def set_theme(self, theme):
        self.config["theme"] = theme
        self.character_system.save_config()
        log.info(f"[Settings][set_theme] 🎨 Theme gesetzt auf: {theme}")

    def set_nsfw(self, state):
        active = state == 2
        self.character_system.nsfw_enabled = active
        self.config["nsfw_enabled"] = active
        self.character_system.save_config()
        log.info(f"[Settings][set_nsfw] 🔞 NSFW-Modus: {'Aktiv' if active else 'Deaktiviert'}")

    def set_controller(self, state):
        active = state == 2
        self.config["controller_enabled"] = active
        self.character_system.save_config()
        log.info(f"[Settings][set_controller] 🎮 Controller: {'Aktiv' if active else 'Deaktiviert'}")

    def toggle_debug_console(self):
        if self.debug_console is None:
            self.debug_console = DebugConsole()
            log.info("[Settings][toggle_debug_console] 🧱 Debug-Konsole initialisiert.")
        self.debug_console.show()
        log.info("[Settings][toggle_debug_console] 🐞 Debug-Konsole angezeigt.")
