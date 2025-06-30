from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtCore import Qt

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📤 Export")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Preset speichern
        self.save_input = QLineEdit()
        self.save_input.setPlaceholderText("🔖 Name für Preset eingeben")
        layout.addWidget(self.save_input)

        save_btn = QPushButton("💾 Preset speichern")
        save_btn.clicked.connect(self.save_preset)
        layout.addWidget(save_btn)

        # Preset laden
        self.load_input = QLineEdit()
        self.load_input.setPlaceholderText("📂 Name für Preset laden")
        layout.addWidget(self.load_input)

        load_btn = QPushButton("📂 Preset laden")
        load_btn.clicked.connect(self.load_preset)
        layout.addWidget(load_btn)

        # Export FBX
        export_btn = QPushButton("📦 FBX exportieren")
        export_btn.clicked.connect(self.export)
        layout.addWidget(export_btn)

        # Statusanzeige
        self.status = QLabel("⏳ Bereit")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.save_input.text().strip()
        if name:
            path = self.character_system.save_preset(name)
            self.status.setText(f"💾 Gespeichert: {path.name}")
        else:
            self.status.setText("⚠️ Kein Presetname angegeben")

    def load_preset(self):
        name = self.load_input.text().strip()
        if name and self.character_system.load_preset(name):
            self.character_system.apply_loaded_state()  # Neu in Block 63
            self.status.setText(f"📂 Geladen: {name}")
        else:
            self.status.setText("❌ Fehler beim Laden")

    def export(self):
        self.status.setText("📦 Export läuft...")
        self.character_system.export_fbx()
        self.status.setText("✅ Export abgeschlossen")