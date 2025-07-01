from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from core.character_system.character_system import CharacterSystem

class SculptPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🪓 Sculpting-Modus"))

        self.symmetry_x = QCheckBox("Symmetrie X")
        self.symmetry_y = QCheckBox("Symmetrie Y")
        self.symmetry_z = QCheckBox("Symmetrie Z")
        layout.addWidget(self.symmetry_x)
        layout.addWidget(self.symmetry_y)
        layout.addWidget(self.symmetry_z)

        btn_start = QPushButton("Sculpting starten")
        btn_start.clicked.connect(self.start_sculpting)
        layout.addWidget(btn_start)

        self.status_label = QLabel("Bereit")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_sculpting(self):
        x = self.symmetry_x.isChecked()
        y = self.symmetry_y.isChecked()
        z = self.symmetry_z.isChecked()
        print(f"[Sculpt] Symmetrie → X:{x} Y:{y} Z:{z}")
        self.status_label.setText("Starte Blender...")
        self.character_system.sculpt()
        self.status_label.setText("Sculpting aktiv (in Blender)")