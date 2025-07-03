from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from core.character_system.character_system import CharacterSystem
import datetime

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
        self.log("[RiggingPanel][__init__] ✅ Panel initialisiert.")

    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        print(f"{timestamp} {msg}")

    def auto_rig(self):
        self.log("[RiggingPanel][auto_rig] ▶️ Starte Auto-Rig...")
        try:
            self.character_system.create_autorig()
            self.log("[RiggingPanel][auto_rig] ✅ Auto-Rig erfolgreich erstellt.")
        except Exception as e:
            self.log(f"[RiggingPanel][auto_rig] ❌ Fehler: {e}")

    def export_metahuman(self):
        self.log("[RiggingPanel][export_metahuman] ▶️ Exportiere Metahuman-Rig...")
        try:
            self.character_system.export_fbx("metahuman_rigged")
            self.log("[RiggingPanel][export_metahuman] ✅ Export abgeschlossen.")
        except Exception as e:
            self.log(f"[RiggingPanel][export_metahuman] ❌ Fehler: {e}")