import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel
from core.character_system.character_system import CharacterSystem

class PresetBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("🎴 Verfügbare Presets:"))

        self.preset_list = QListWidget()
        self.refresh_presets()
        self.layout.addWidget(self.preset_list)

        btn_load = QPushButton("Ausgewähltes Preset laden")
        btn_load.clicked.connect(self.load_selected)
        self.layout.addWidget(btn_load)

        btn_refresh = QPushButton("Liste aktualisieren")
        btn_refresh.clicked.connect(self.refresh_presets)
        self.layout.addWidget(btn_refresh)

    def refresh_presets(self):
        self.preset_list.clear()
        if not os.path.exists("presets/"):
            os.makedirs("presets/")
        files = [f for f in os.listdir("presets/") if f.endswith(".json")]
        self.preset_list.addItems([f.replace(".json", "") for f in files])

    def load_selected(self):
        selected = self.preset_list.currentItem()
        if selected:
            name = selected.text()
            self.character_system.load_preset(name)