from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit
from core.character_system.character_system import CharacterSystem

class ExportPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Preset-/Export-Name eingeben")
        self.export_log = QTextEdit()
        self.export_log.setReadOnly(True)

        btn_save = QPushButton("Preset speichern")
        btn_export = QPushButton("Exportiere .FBX")

        btn_save.clicked.connect(self.save_preset)
        btn_export.clicked.connect(self.export_fbx)

        layout.addWidget(QLabel("Export & Presets"))
        layout.addWidget(self.name_input)
        layout.addWidget(btn_save)
        layout.addWidget(btn_export)
        layout.addWidget(QLabel("Status / Log:"))
        layout.addWidget(self.export_log)

        self.setLayout(layout)

    def save_preset(self):
        name = self.name_input.text() or "default"
        self.character_system.save_preset(name)
        self.export_log.append(f"[Preset] Gespeichert als: {name}.json")

    def export_fbx(self):
        name = self.name_input.text() or "exported_character"
        self.export_log.append(f"[Export] Starte FBX-Export: {name}.fbx")
        self.character_system.export_fbx(name)
        self.export_log.append(f"[Export] Erfolgreich exportiert.")