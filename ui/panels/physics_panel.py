from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from core.character_system.character_system import CharacterSystem
from core.logger import log

class PhysicsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        log("[PhysicsPanel][__init__] ▶️ Initialisiere Panel...", "INFO")

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
        log("[PhysicsPanel][__init__] ✅ Panel bereit.", "SUCCESS")

    def toggle(self, key, state):
        new_value = (state == 2)
        self.character_system.physics_flags[key] = new_value
        log(f"[PhysicsPanel][toggle] ▶️ {key} = {new_value}", "INFO")