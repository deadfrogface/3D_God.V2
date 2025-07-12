from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QFileDialog, QHBoxLayout, QMessageBox
)
from core.logger import log
from core.ai_generation.ai_generator import AIGenerator
import os

class AIPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.generator = AIGenerator(character_system=self.character_system)
        self.selected_image_path = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🧠 Text- oder Bildbasierte 3D-Modellerzeugung"))

        # Text Prompt Eingabe
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("z. B. 'muscular elf warrior' oder 'lederhose'…")
        layout.addWidget(self.prompt_input)

        # Bildauswahl
        img_row = QHBoxLayout()
        self.image_path_label = QLabel("📂 Kein Bild ausgewählt")
        btn_image = QPushButton("Bild laden")
        btn_image.clicked.connect(self.handle_image)
        img_row.addWidget(self.image_path_label)
        img_row.addWidget(btn_image)
        layout.addLayout(img_row)

        # Auswahl Buttons
        btn_person = QPushButton("👤 Erzeuge vollständige Person")
        btn_person.clicked.connect(self.generate_full_character)
        layout.addWidget(btn_person)

        btn_asset = QPushButton("📦 Erzeuge Asset (z. B. Kleidung)")
        btn_asset.clicked.connect(self.generate_asset)
        layout.addWidget(btn_asset)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # Codeausgabe (optional sichtbar)
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)
        self.code_output.setVisible(False)
        layout.addWidget(self.code_output)

        self.setLayout(layout)
        log.info("[AIPanel][__init__] ✅ Initialisiert")

    def handle_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "", "Bilder (*.png *.jpg *.jpeg)")
        if path:
            self.selected_image_path = path
            self.image_path_label.setText(os.path.basename(path))
            self.generator.set_image_path(path)
            self.status_label.setText("📸 Bild ausgewählt.")
            log.info(f"[AIPanel][handle_image] ✅ Bild: {path}")
        else:
            self.status_label.setText("⚠️ Kein Bild ausgewählt.")

    def generate_full_character(self):
        try:
            self.status_label.setText("🌀 Generiere vollständiges 3D-Modell...")
            self.repaint()

            prompt = self.prompt_input.text().strip() or None
            image = self.selected_image_path

            result_path = self.generator.generate_full_character(prompt=prompt, image_path=image)

            if result_path and os.path.exists(result_path):
                self.character_system.viewport_ref.load_preview(result_path)
                self.status_label.setText(f"✅ Modell geladen: {os.path.basename(result_path)}")
                log.success(f"[AIPanel] ✅ Modell erzeugt: {result_path}")
            else:
                raise RuntimeError("Kein Modell erzeugt")
        except Exception as e:
            log.error(f"[AIPanel][generate_full_character] ❌ Fehler: {e}")
            self.status_label.setText(f"❌ Fehler: {e}")

    def generate_asset(self):
        try:
            self.status_label.setText("🌀 Generiere Asset...")
            self.repaint()

            prompt = self.prompt_input.text().strip() or None
            image = self.selected_image_path

            result_path = self.generator.generate_asset(prompt=prompt, image_path=image)

            if result_path and os.path.exists(result_path):
                self.character_system.viewport_ref.load_preview(result_path)
                self.status_label.setText(f"✅ Asset geladen: {os.path.basename(result_path)}")
                log.success(f"[AIPanel] ✅ Asset erzeugt: {result_path}")
            else:
                raise RuntimeError("Kein Asset erzeugt")
        except Exception as e:
            log.error(f"[AIPanel][generate_asset] ❌ Fehler: {e}")
            self.status_label.setText(f"❌ Fehler: {e}")
