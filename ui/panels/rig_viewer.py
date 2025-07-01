from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
import os
import json

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

    def load_bones(self):
        bone_path = os.path.join("exports", "last_bone_export.json")
        self.bone_list.clear()

        if os.path.exists(bone_path):
            with open(bone_path, "r") as f:
                bones = json.load(f)
                for bone in bones:
                    self.bone_list.addItem(bone)
            print(f"[RigViewer] {len(bones)} Bones geladen.")
        else:
            self.bone_list.addItem("Keine Rig-Daten gefunden.")
            print("[RigViewer] Datei nicht gefunden:", bone_path)