from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from core.character_system.character_system import CharacterSystem

class ExportPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.status = QLabel("Exportstatus: Noch nichts exportiert.")
        layout.addWidget(self.status)

        export_btn = QPushButton("📦 Exportiere Modell als FBX")
        export_btn.clicked.connect(self.export_model)
        layout.addWidget(export_btn)

        self.setLayout(layout)

    def export_model(self):
        self.status.setText("🔄 Export läuft...")
        self.character_system.export_model()
        self.status.setText("✅ Export abgeschlossen (exports/final_model.fbx)")