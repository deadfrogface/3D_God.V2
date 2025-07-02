from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit
)
from core.character_system.character_system import CharacterSystem
import datetime

class ExportPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("📦 Modell-Export"))

        self.name_input = QLineEdit("my_character")
        layout.addWidget(self.name_input)

        self.logbox = QTextEdit()
        self.logbox.setReadOnly(True)
        self.logbox.setPlaceholderText("📝 Export-Meldungen...")
        layout.addWidget(self.logbox)

        btn_save = QPushButton("💾 Preset speichern")
        btn_save.clicked.connect(self.save_preset)
        layout.addWidget(btn_save)

        btn_export = QPushButton("📤 FBX exportieren")
        btn_export.clicked.connect(self.export_fbx)
        layout.addWidget(btn_export)

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
            self.log("✅ FBX-Export abgeschlossen.")
        except Exception as e:
            self.log(f"❌ Fehler beim Export: {e}")