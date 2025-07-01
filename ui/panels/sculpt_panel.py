from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from core.character_system.character_system import CharacterSystem

class SculptPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.btn_sculpt = QPushButton("Sculpting starten")
        self.btn_script = QPushButton("Blender-Skript ausführen")

        self.btn_sculpt.clicked.connect(self.character_system.sculpt)
        self.btn_script.clicked.connect(lambda: self.character_system.run_blender_script("apply_symmetry.py"))

        layout.addWidget(self.btn_sculpt)
        layout.addWidget(self.btn_script)
        self.setLayout(layout)
