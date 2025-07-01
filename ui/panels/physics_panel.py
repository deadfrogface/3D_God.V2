from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from core.character_system.character_system import CharacterSystem

class PhysicsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("⚙️ Physikoptionen"))

        self.check_breasts = QCheckBox("🫃 Brustphysik (Softbody)")
        self.check_breasts.setChecked(self.character_system.physics_flags.get("breasts", True))
        self.check_breasts.stateChanged.connect(lambda state: self.toggle("breasts", state))
        layout.addWidget(self.check_breasts)

        self.check_cloth = QCheckBox("👕 Stoffsimulation (Kleidung)")
        self.check_cloth.setChecked(self.character_system.physics_flags.get("cloth", True))
        self.check_cloth.stateChanged.connect(lambda state: self.toggle("cloth", state))
        layout.addWidget(self.check_cloth)

        self.check_piercing = QCheckBox("📎 Piercing-Schwingung")
        self.check_piercing.setChecked(self.character_system.physics_flags.get("piercings", True))
        self.check_piercing.stateChanged.connect(lambda state: self.toggle("piercings", state))
        layout.addWidget(self.check_piercing)

        self.setLayout(layout)

    def toggle(self, key, state):
        self.character_system.physics_flags[key] = (state == 2)
        print(f"[Physik] {key} = {self.character_system.physics_flags[key]}")