from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("📤 Export zu Unreal Engine 5.6")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Preset speichern
        save_layout = QHBoxLayout()
        self.save_name = QLineEdit()
        self.save_name.setPlaceholderText("Name für Preset...")
        save_btn = QPushButton("💾 Preset speichern")
        save_btn.clicked.connect(self.save_preset)
        save_layout.addWidget(self.save_name)
        save_layout.addWidget(save_btn)
        layout.addLayout(save_layout)

        # Preset laden
        load_layout = QHBoxLayout()
        self.load_box = QComboBox()
        self.update_preset_list()
        load_btn = QPushButton("📂 Preset laden")
        load_btn.clicked.connect(self.load_preset)
        load_layout.addWidget(self.load_box)
        load_layout.addWidget(load_btn)
        layout.addLayout(load_layout)

        # Export starten
        export_btn = QPushButton("📦 FBX Export")
        export_btn.clicked.connect(self.export)
        layout.addWidget(export_btn)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.save_name.text().strip()
        if not name:
            print("⚠️ Kein Name eingegeben.")
            return
        path = self.character_system.save_preset(name)
        print(f"✅ Preset gespeichert: {path}")
        self.update_preset_list()

    def load_preset(self):
        name = self.load_box.currentText()
        if self.character_system.load_preset(name):
            print(f"✅ Preset geladen: {name}")
        else:
            print(f"❌ Fehler beim Laden von: {name}")

    def update_preset_list(self):
        self.load_box.clear()
        path = self.character_system.preset_path
        if path.exists():
            presets = [f.stem for f in path.glob("*.json")]
            self.load_box.addItems(presets)

    def export(self):
        self.character_system.export_fbx()