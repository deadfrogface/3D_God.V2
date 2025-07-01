from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from core.character_system.character_system import CharacterSystem

class ClothingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kleidung:"))
        btn_clothes = QPushButton("Lade Kleidung")
        btn_clothes.clicked.connect(lambda: self.character_system.add_asset("clothes"))
        layout.addWidget(btn_clothes)

        layout.addWidget(QLabel("Piercings:"))
        btn_piercings = QPushButton("Lade Piercings")
        btn_piercings.clicked.connect(lambda: self.character_system.add_asset("piercings"))
        layout.addWidget(btn_piercings)

        layout.addWidget(QLabel("Tattoos:"))
        btn_tattoos = QPushButton("Lade Tattoos")
        btn_tattoos.clicked.connect(lambda: self.character_system.add_asset("tattoos"))
        layout.addWidget(btn_tattoos)

        self.setLayout(layout)