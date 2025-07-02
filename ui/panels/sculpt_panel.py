from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from core.character_system.character_system import CharacterSystem

class SculptPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🗿 Sculpting-Modus"))

        # 🔁 Symmetrie-Option
        self.symmetry_toggle = QCheckBox("🔁 X-Achsensymmetrie aktivieren")
        self.symmetry_toggle.setChecked(True)
        self.symmetry_toggle.stateChanged.connect(self.set_symmetry)
        layout.addWidget(self.symmetry_toggle)

        # 🎨 Sculpt starten
        self.btn_start = QPushButton("🎨 Starte Sculpting")
        self.btn_start.clicked.connect(self.start_sculpt)
        layout.addWidget(self.btn_start)

        # 📝 Status-Anzeige
        self.status_label = QLabel("⏹ Nicht aktiv")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_symmetry(self, state):
        self.character_system.sculpt_data["symmetry"] = bool(state)
        print(f"[Sculpt] Symmetrie: {'Aktiv' if state else 'Aus'}")

    def start_sculpt(self):
        self.status_label.setText("⏳ Sculpting wird geladen...")
        self.character_system.sculpt()
        self.status_label.setText("✅ Sculpting-Modus aktiv (in Blender)")