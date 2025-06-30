from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📤 Export-Panel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Preset speichern
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name für Preset (z. B. brakka)")
        layout.addWidget(self.name_input)

        save_btn = QPushButton("💾 Preset speichern")
        save_btn.clicked.connect(self.save_preset)
        layout.addWidget(save_btn)

        # FBX Export starten
        export_btn = QPushButton("📦 FBX Export starten")
        export_btn.clicked.connect(self.export_fbx)
        layout.addWidget(export_btn)

        self.status = QLabel("Bereit")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.name_input.text().strip()
        if not name:
            name = "custom"
        path = self.character_system.save_preset(name)
        self.status.setText(f"✅ Preset gespeichert: {path.name}")

    def export_fbx(self):
        self.character_system.export_fbx()
        self.status.setText("📦 Export läuft (siehe Konsole)...")