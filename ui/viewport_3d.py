from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class Viewport3D(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.status = QLabel("🖼️ 3D-Vorschau (Platzhalter)")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def update_view(self):
        # Später: Mesh laden und anzeigen
        print("🔄 Viewport aktualisieren... (stub)")