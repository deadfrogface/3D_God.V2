from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ClothingPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("👕 Kleidung & Assets")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        btn1 = QPushButton("👔 Kleidung laden")
        btn2 = QPushButton("💍 Piercings hinzufügen")
        btn3 = QPushButton("🎨 Tattoos anzeigen")

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        layout.addStretch()
        self.setLayout(layout)