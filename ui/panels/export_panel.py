from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from core.character_system.character_system import CharacterSystem
import os
import shutil

class ExportPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("💾 Export-Optionen"))

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Dateiname:"))
        self.name_input = QLineEdit("my_character")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        btn_save = QPushButton("Preset speichern")
        btn_save.clicked.connect(self.save_preset)
        layout.addWidget(btn_save)

        btn_export = QPushButton("Exportiere als .fbx")
        btn_export.clicked.connect(self.export_fbx)
        layout.addWidget(btn_export)

        layout.addWidget(QLabel("📦 Export nach Unreal-Projekt"))

        self.unreal_path = QLineEdit("")
        self.unreal_path.setPlaceholderText("Pfad zum Unreal Content-Ordner (z. B. .../YourProject/Content/Characters)")
        layout.addWidget(self.unreal_path)

        btn_browse = QPushButton("Ziel auswählen")
        btn_browse.clicked.connect(self.choose_unreal_folder)
        layout.addWidget(btn_browse)

        btn_unreal = QPushButton("Exportiere direkt nach Unreal")
        btn_unreal.clicked.connect(self.export_to_unreal)
        layout.addWidget(btn_unreal)

        self.setLayout(layout)

    def save_preset(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)

    def export_fbx(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)
        self.character_system.export_fbx(name)

    def choose_unreal_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Unreal Content-Ordner wählen")
        if path:
            self.unreal_path.setText(path)

    def export_to_unreal(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)
        self.character_system.export_fbx(name)

        src_fbx = os.path.join("exports", f"{name}.fbx")
        dst_dir = self.unreal_path.text().strip()
        if not dst_dir or not os.path.exists(dst_dir):
            print("[Export] Ungültiger Unreal-Pfad")
            return

        dst_fbx = os.path.join(dst_dir, f"{name}.fbx")
        shutil.copy(src_fbx, dst_fbx)
        print(f"[Export → Unreal] Datei kopiert nach: {dst_fbx}")