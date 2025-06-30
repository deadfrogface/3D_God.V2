from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Qt

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📤 Export Panel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Preset speichern
        self.save_name = QLineEdit()
        self.save_name.setPlaceholderText("Preset-Name eingeben")
        layout.addWidget(self.save_name)

        save_btn = QPushButton("💾 Preset speichern")
        save_btn.clicked.connect(self.save_preset)
        layout.addWidget(save_btn)

        # Preset laden
        self.load_name = QLineEdit()
        self.load_name.setPlaceholderText("Preset-Name zum Laden")
        layout.addWidget(self.load_name)

        load_btn = QPushButton("📂 Preset laden")
        load_btn.clicked.connect(self.load_preset)
        layout.addWidget(load_btn)

        # FBX Export
        export_btn = QPushButton("📦 FBX exportieren")
        export_btn.clicked.connect(self.character_system.export_fbx)
        layout.addWidget(export_btn)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.save_name.text().strip()
        if name:
            path = self.character_system.save_preset(name)
            print(f"💾 Preset gespeichert: {path}")

    def load_preset(self):
        name = self.load_name.text().strip()
        if name:
            if self.character_system.load_preset(name):
                print(f"📂 Preset geladen: {name}")
            else:
                print(f"❌ Fehler beim Laden: {name}")