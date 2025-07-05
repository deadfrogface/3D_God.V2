from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from core.logger import log

class ClothingPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kleidung:"))
        btn_clothes = QPushButton("Lade Kleidung")
        btn_clothes.clicked.connect(self.load_clothes)
        layout.addWidget(btn_clothes)

        layout.addWidget(QLabel("Piercings:"))
        btn_piercings = QPushButton("Lade Piercings")
        btn_piercings.clicked.connect(self.load_piercings)
        layout.addWidget(btn_piercings)

        layout.addWidget(QLabel("Tattoos:"))
        btn_tattoos = QPushButton("Lade Tattoos")
        btn_tattoos.clicked.connect(self.load_tattoos)
        layout.addWidget(btn_tattoos)

        self.setLayout(layout)
        log.info("[ClothingPanel][__init__] ✅ Panel initialisiert")

    def load_clothes(self):
        log.info("[ClothingPanel][load_clothes] ▶️ Lade Kleidung")
        self.character_system.add_asset("clothes")

    def load_piercings(self):
        log.info("[ClothingPanel][load_piercings] ▶️ Lade Piercings")
        self.character_system.add_asset("piercings")

    def load_tattoos(self):
        log.info("[ClothingPanel][load_tattoos] ▶️ Lade Tattoos")
        self.character_system.add_asset("tattoos")
