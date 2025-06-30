from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QFileDialog, QLineEdit, QProgressBar
)
import os

class AIGeneratorPanel(QWidget):
    def __init__(self, ai_generator):
        super().__init__()
        self.ai_generator = ai_generator
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🤖 KI-Generator"))

        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("📝 Text-Prompt eingeben...")
        layout.addWidget(self.prompt_input)

        self.type_box = QComboBox()
        self.type_box.addItems(["Charakter", "Kleidung", "Asset"])
        layout.addWidget(self.type_box)

        self.image_button = QPushButton("🖼️ Bild auswählen")
        self.image_button.clicked.connect(self.select_image)
        layout.addWidget(self.image_button)

        self.generate_button = QPushButton("⚡ Generieren")
        self.generate_button.clicked.connect(self.start_generation)
        layout.addWidget(self.generate_button)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.status.setMaximumHeight(120)
        layout.addWidget(self.status)

        self.setLayout(layout)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Bild auswählen", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self.image_path = path
            self.log(f"🖼️ Bild geladen: {os.path.basename(path)}")

    def start_generation(self):
        prompt = self.prompt_input.text().strip()
        asset_type = self.type_box.currentText()

        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.generate_button.setEnabled(False)

        self.log("🧠 Starte KI-Generierung...")
        try:
            output_path = self.ai_generator.generate(prompt, self.image_path, asset_type)
            self.log(f"✅ 3D-Modell gespeichert: {output_path}")
        except Exception as e:
            self.log(f"❌ Fehler: {e}")
        finally:
            self.progress.setVisible(False)
            self.generate_button.setEnabled(True)

    def log(self, msg):
        self.status.append(msg)
