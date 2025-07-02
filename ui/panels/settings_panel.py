from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QTextEdit
from core.character_system.character_system import CharacterSystem
import os
import shutil
import datetime

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

        btn_save = QPushButton("💾 Preset speichern")
        btn_save.clicked.connect(self.save_preset)
        layout.addWidget(btn_save)

        btn_export = QPushButton("📤 Exportiere als .fbx")
        btn_export.clicked.connect(self.export_fbx)
        layout.addWidget(btn_export)

        layout.addWidget(QLabel("📦 Export nach Unreal-Projekt"))

        self.unreal_path = QLineEdit("")
        self.unreal_path.setPlaceholderText("Pfad zu /YourGame/Content/Characters")
        layout.addWidget(self.unreal_path)

        btn_browse = QPushButton("📁 Ziel auswählen")
        btn_browse.clicked.connect(self.choose_unreal_folder)
        layout.addWidget(btn_browse)

        btn_unreal = QPushButton("🚀 Exportiere direkt nach Unreal")
        btn_unreal.clicked.connect(self.export_to_unreal)
        layout.addWidget(btn_unreal)

        layout.addWidget(QLabel("📋 Export-Log:"))
        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        layout.addWidget(self.logbox)

        self.setLayout(layout)

    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{timestamp} {msg}"
        self.logbox.append(full_msg)
        print(full_msg)
        with open("logfile.txt", "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")

    def save_preset(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)
        self.log(f"✔ Preset gespeichert: {name}")

    def export_fbx(self):
        name = self.name_input.text()
        self.log("📤 Starte Export...")
        self.character_system.save_preset(name)
        self.character_system.export_fbx(name)
        self.log(f"✅ FBX exportiert: exports/{name}.fbx")

    def choose_unreal_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Unreal Content-Ordner wählen")
        if path:
            self.unreal_path.setText(path)
            self.log(f"📁 Ziel ausgewählt: {path}")

    def export_to_unreal(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)
        self.character_system.export_fbx(name)

        src_fbx = os.path.join("exports", f"{name}.fbx")
        dst_dir = self.unreal_path.text().strip()
        if not dst_dir or not os.path.exists(dst_dir):
            self.log("❌ Fehler: Unreal-Zielpfad ungültig.")
            return

        dst_fbx = os.path.join(dst_dir, f"{name}.fbx")
        try:
            shutil.copy(src_fbx, dst_fbx)
            self.log(f"✅ FBX kopiert nach Unreal: {dst_fbx}")
        except Exception as e:
            self.log(f"❌ Kopierfehler: {e}")