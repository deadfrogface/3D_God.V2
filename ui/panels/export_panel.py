from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        layout = QVBoxLayout()

        self.label = QLabel("📤 Exportieren")
        layout.addWidget(self.label)

        export_btn = QPushButton("💾 FBX Exportieren")
        export_btn.clicked.connect(self.export_fbx)
        layout.addWidget(export_btn)

        preset_btn = QPushButton("📝 Preset speichern")
        preset_btn.clicked.connect(self.save_preset)
        layout.addWidget(preset_btn)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def export_fbx(self):
        path = self.character_system.export_to_file()
        self.status.setText(f"✅ Exportiert: {path}")

    def save_preset(self):
        path = self.character_system.save_current_as_preset()
        self.status.setText(f"💾 Preset gespeichert: {path}")
