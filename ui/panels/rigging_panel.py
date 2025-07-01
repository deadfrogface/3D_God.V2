from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from core.character_system.character_system import CharacterSystem

class RiggingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.btn_autorig = QPushButton("Auto-Rigging (Standard)")
        self.btn_metahuman = QPushButton("Metahuman-Rig vorbereiten")
        self.btn_custom = QPushButton("Manuelles Rigging-Skript ausführen")

        self.btn_autorig.clicked.connect(lambda: self.character_system.run_blender_script("autorig_basic.py"))
        self.btn_metahuman.clicked.connect(lambda: self.character_system.run_blender_script("metahuman_rig.py"))
        self.btn_custom.clicked.connect(lambda: self.character_system.run_blender_script("custom_rig.py"))

        layout.addWidget(self.btn_autorig)
        layout.addWidget(self.btn_metahuman)
        layout.addWidget(self.btn_custom)
        self.setLayout(layout)