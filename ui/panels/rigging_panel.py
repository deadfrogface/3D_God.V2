from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from core.logger import log

class RiggingPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🦴 Rigging & Skeleton Setup"))

        btn_auto = QPushButton("Auto-Rig erstellen")
        btn_auto.clicked.connect(self.auto_rig)
        layout.addWidget(btn_auto)

        btn_metahuman = QPushButton("Metahuman-kompatibles Rig exportieren")
        btn_metahuman.clicked.connect(self.export_metahuman)
        layout.addWidget(btn_metahuman)

        self.setLayout(layout)
        log.info("[RiggingPanel][__init__] ✅ Panel initialisiert.")

    def auto_rig(self):
        log.info("[RiggingPanel][auto_rig] ▶️ Starte Auto-Rig...")
        try:
            self.character_system.create_autorig()
            log.info("[RiggingPanel][auto_rig] ✅ Auto-Rig erfolgreich erstellt.")
        except Exception as e:
            log.error(f"[RiggingPanel][auto_rig] ❌ Fehler: {e}")

    def export_metahuman(self):
        log.info("[RiggingPanel][export_metahuman] ▶️ Exportiere Metahuman-Rig...")
        try:
            self.character_system.export_fbx("metahuman_rigged")
            log.info("[RiggingPanel][export_metahuman] ✅ Export abgeschlossen.")
        except Exception as e:
            log.error(f"[RiggingPanel][export_metahuman] ❌ Fehler: {e}")
