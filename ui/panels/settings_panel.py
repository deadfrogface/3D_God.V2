from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from core.character_system.character_system import CharacterSystem
from ui.debug_console import DebugConsole

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        self.debug_console = None

        layout = QVBoxLayout()
        layout.addWidget(QLabel("⚙ Einstellungen"))

        # 🌙 Theme
        self.theme_checkbox = QCheckBox("🌙 Dunkles Design aktivieren")
        self.theme_checkbox.setChecked(self.character_system.config.get("theme", "dark") == "dark")
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_checkbox)

        # 🔞 NSFW
        self.nsfw_checkbox = QCheckBox("🔞 NSFW-Modus aktivieren")
        self.nsfw_checkbox.setChecked(self.character_system.nsfw_enabled)
        self.nsfw_checkbox.stateChanged.connect(self.toggle_nsfw)
        layout.addWidget(self.nsfw_checkbox)

        # 🎮 Controller
        self.controller_checkbox = QCheckBox("🎮 Controller-Unterstützung")
        self.controller_checkbox.setChecked(self.character_system.config.get("controller_enabled", True))
        self.controller_checkbox.stateChanged.connect(self.toggle_controller)
        layout.addWidget(self.controller_checkbox)

        # 🐞 Debug-Konsole
        btn_debug = QPushButton("🐞 Debug-Konsole anzeigen")
        btn_debug.clicked.connect(self.toggle_debug_console)
        layout.addWidget(btn_debug)

        self.setLayout(layout)

    def toggle_theme(self, state):
        theme = "dark" if state else "light"
        self.character_system.config["theme"] = theme
        self.character_system.save_config()
        print(f"[Settings] Theme geändert zu: {theme}")

    def toggle_nsfw(self, state):
        self.character_system.nsfw_enabled = bool(state)
        self.character_system.config["nsfw_enabled"] = bool(state)
        self.character_system.save_config()
        print(f"[Settings] NSFW-Modus: {'Aktiv' if state else 'Deaktiviert'}")

    def toggle_controller(self, state):
        self.character_system.config["controller_enabled"] = bool(state)
        self.character_system.save_config()
        print(f"[Settings] Controller: {'Aktiv' if state else 'Deaktiviert'}")

    def toggle_debug_console(self):
        if self.debug_console is None:
            self.debug_console = DebugConsole()
        self.debug_console.show()