from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
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

        # Preset Name Eingabe
        preset_layout = QHBoxLayout()
        self.preset_input = QLineEdit()
        self.preset_input.setPlaceholderText("Name für Preset...")
        save_preset_btn = QPushButton("💾 Preset speichern")
        save_preset_btn.clicked.connect(self.save_preset)
        preset_layout.addWidget(self.preset_input)
        preset_layout.addWidget(save_preset_btn)
        layout.addLayout(preset_layout)

        # Export Button
        export_btn = QPushButton("📦 Exportiere als FBX")
        export_btn.clicked.connect(self.export_fbx)
        layout.addWidget(export_btn)

        # Statusanzeige
        self.status = QLabel("")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.preset_input.text().strip()
        if not name:
            self.status.setText("❌ Bitte einen Namen für das Preset angeben.")
            return

        path = self.character_system.save_preset(name)
        self.status.setText(f"✅ Preset gespeichert: {path}")

    def export_fbx(self):
        self.status.setText("🚀 Exportiere als FBX...")
        self.character_system.export_fbx()
        self.status.setText("✅ FBX-Export abgeschlossen.")