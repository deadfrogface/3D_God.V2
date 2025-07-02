from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QHBoxLayout
)
from core.character_system.character_system import CharacterSystem
import os
import shutil
import datetime

class ExportPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("📦 Modell-Export"))

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Dateiname:"))
        self.name_input = QLineEdit("my_character")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        btn_save = QPushButton("💾 Preset speichern")
        btn_save.clicked.connect(self.save_preset)
        layout.addWidget(btn_save)

        btn_export = QPushButton("📤 FBX exportieren")
        btn_export.clicked.connect(self.export_fbx)
        layout.addWidget(btn_export)

        layout.addWidget(QLabel("📂 Unreal-Zielordner"))
        self.unreal_path = QLineEdit("")
        self.unreal_path.setPlaceholderText("z. B. C:/Projekte/UE5/YourGame/Content/Characters")
        layout.addWidget(self.unreal_path)

        btn_browse = QPushButton("📁 Ordner wählen")
        btn_browse.clicked.connect(self.choose_unreal_folder)
        layout.addWidget(btn_browse)

        btn_unreal = QPushButton("🚀 Exportiere nach Unreal")
        btn_unreal.clicked.connect(self.export_to_unreal)
        layout.addWidget(btn_unreal)

        layout.addWidget(QLabel("📝 Export-Log"))
        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setPlaceholderText("Exportmeldungen erscheinen hier...")
        layout.addWidget(self.logbox)

        self.setLayout(layout)

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        entry = f"{timestamp} {message}"
        self.logbox.append(entry)
        print(entry)
        with open("logfile.txt", "a", encoding="utf-8") as f:
            f.write(entry + "\n")

    def save_preset(self):
        name = self.name_input.text()
        self.character_system.save_preset(name)
        self.log(f"✅ Preset gespeichert: {name}")

    def export_fbx(self):
        name = self.name_input.text()
        self.log("🚀 Starte Export...")
        try:
            self.character_system.save_preset(name)
            self.character_system.export_model()
            self.log(f"✅ FBX-Export abgeschlossen: exports/{name}.fbx")

            # Vorschau aktualisieren (falls vorhanden)
            if self.character_system.viewport_ref:
                self.character_system.viewport_ref.load_preview("exports/preview.glb")
                self.log("🖼️ Vorschau aktualisiert.")
        except Exception as e:
            self.log(f"❌ Fehler beim Export: {e}")

    def choose_unreal_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Unreal-Zielordner wählen")
        if path:
            self.unreal_path.setText(path)
            self.log(f"📁 Unreal-Zielordner: {path}")

    def export_to_unreal(self):
        name = self.name_input.text()
        src_fbx = os.path.join("exports", f"{name}.fbx")
        dst_dir = self.unreal_path.text().strip()

        if not dst_dir or not os.path.exists(dst_dir):
            self.log("❌ Fehler: Ungültiger Unreal-Zielpfad.")
            return

        try:
            dst_fbx = os.path.join(dst_dir, f"{name}.fbx")
            shutil.copy(src_fbx, dst_fbx)
            self.log(f"✅ FBX kopiert nach Unreal: {dst_fbx}")
        except Exception as e:
            self.log(f"❌ Fehler beim Kopieren: {e}")