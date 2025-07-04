from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from core.character_system.character_system import CharacterSystem
from core.logger import log

class SculptPanel(QWidget):
    def __init__(self, character_system: CharacterSystem):
        super().__init__()
        self.character_system = character_system
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🗿 Sculpting-Modus"))

        # 🔁 Symmetrie-Option
        self.symmetry_toggle = QCheckBox("🔁 X-Achsensymmetrie aktivieren")
        self.symmetry_toggle.setChecked(self.character_system.sculpt_data.get("symmetry", True))
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
        log.info("[SculptPanel][__init__] ✅ Initialisiert.")

    def set_symmetry(self, state):
        active = (state == 2)
        self.character_system.sculpt_data["symmetry"] = active
        log.info(f"[SculptPanel][set_symmetry] 🔁 Symmetrie: {'Aktiv' if active else 'Deaktiviert'}")

    def start_sculpt(self):
        self.status_label.setText("⏳ Sculpting wird geladen...")
        log.info("[SculptPanel][start_sculpt] ▶️ Starte Sculpting...")
        self.character_system.sculpt()
        self.status_label.setText("✅ Sculpting-Modus aktiv (in Blender)")
        log.info("[SculptPanel][start_sculpt] ✅ Sculpting-Vorgang abgeschlossen.")
