from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QProgressBar, QTextEdit, QMessageBox
)

class ExportPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("📤 Export & Preset"))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name des Presets eingeben ...")
        layout.addWidget(self.name_input)

        save_btn = QPushButton("💾 Preset speichern")
        save_btn.clicked.connect(self.save_preset)
        layout.addWidget(save_btn)

        export_btn = QPushButton("📤 FBX Export starten")
        export_btn.clicked.connect(self.export_fbx)
        layout.addWidget(export_btn)

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)  # Unbestimmter Fortschritt
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(200)
        layout.addWidget(self.log_output)

        layout.addStretch()
        self.setLayout(layout)

    def save_preset(self):
        name = self.name_input.text().strip() or "custom"
        path = self.character_system.save_preset(name)
        QMessageBox.information(self, "Preset gespeichert", f"{name}.json wurde gespeichert in:\n{path}")
        self.log(f"💾 Preset gespeichert als: {name}.json")

    def export_fbx(self):
        self.progress.setVisible(True)
        self.log("📤 Starte FBX-Export...")

        try:
            self.character_system.export_fbx()
            self.log("✅ FBX erfolgreich exportiert!")
        except Exception as e:
            self.log(f"❌ Fehler: {str(e)}")

        self.progress.setVisible(False)

    def log(self, text):
        self.log_output.append(text)