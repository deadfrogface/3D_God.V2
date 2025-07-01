from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from core.character_system.character_system import CharacterSystem

class RiggingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🦴 Rigging & Skeleton Setup"))

        btn_auto = QPushButton("Auto-Rig erstellen")
        btn_auto.clicked.connect(self.auto_rig)
        layout.addWidget(btn_auto)

        btn_metahuman = QPushButton("Metahuman-kompatibles Rig exportieren")
        btn_metahuman.clicked.connect(self.export_metahuman)
        layout.addWidget(btn_metahuman)

        self.setLayout(layout)

    def auto_rig(self):
        self.character_system.create_autorig()

    def export_metahuman(self):
        self.character_system.export_fbx("metahuman_rigged")