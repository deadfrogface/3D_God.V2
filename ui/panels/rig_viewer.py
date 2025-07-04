from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
import os
import json
from core.logger import log  # ← Verwende das zentrale Logging

class RigViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🦴 Aktuelles Rig (Bone-Struktur)"))

        self.bone_list = QListWidget()
        layout.addWidget(self.bone_list)

        self.refresh_btn = QPushButton("Aktuelle Bones anzeigen")
        self.refresh_btn.clicked.connect(self.load_bones)
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)
        log("[RigViewer][__init__] ✅ Panel initialisiert", "INFO")

    def load_bones(self):
        bone_path = os.path.join("exports", "last_bone_export.json")
        self.bone_list.clear()
        log(f"[RigViewer][load_bones] ▶️ Lade Datei: {bone_path}", "INFO")

        if os.path.exists(bone_path):
            try:
                with open(bone_path, "r") as f:
                    bones = json.load(f)
                    for bone in bones:
                        self.bone_list.addItem(bone)
                log(f"[RigViewer][load_bones] ✅ {len(bones)} Bones geladen.", "SUCCESS")
            except Exception as e:
                self.bone_list.addItem("❌ Fehler beim Lesen der Datei.")
                log(f"[RigViewer][load_bones] ❌ JSON-Lesefehler: {e}", "ERROR")
        else:
            self.bone_list.addItem("Keine Rig-Daten gefunden.")
            log(f"[RigViewer][load_bones] ❌ Datei nicht gefunden: {bone_path}", "ERROR")