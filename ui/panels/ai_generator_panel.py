from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QHBoxLayout
)
from core.ai_generation.ai_generator import AIGenerator
from core.logger import log
import os

class AIPromptPanel(QWidget):
    def __init__(self, character_system):
        try:
            super().__init__()
            self.character_system = character_system
            self.generator = AIGenerator(character_system=self.character_system)
            self.selected_image_path = None

            layout = QVBoxLayout()
            layout.addWidget(QLabel("🧠 Text → Code (FauxPilot)"))

            self.text_input = QTextEdit()
            self.text_input.setPlaceholderText("Was soll die KI schreiben? (z. B. Blender-Skript, Material, Rig...)")
            layout.addWidget(self.text_input)

            self.text_output = QTextEdit()
            self.text_output.setReadOnly(True)
            layout.addWidget(self.text_output)

            btn_generate = QPushButton("🧠 Code generieren")
            btn_generate.clicked.connect(self.handle_generate)
            layout.addWidget(btn_generate)

            layout.addWidget(QLabel("🖼️ Bild → Mesh (TripoSR)"))
            image_layout = QHBoxLayout()
            self.image_path_label = QLabel("📂 Kein Bild gewählt")
            btn_image = QPushButton("Bild auswählen")
            btn_image.clicked.connect(self.handle_image)
            image_layout.addWidget(self.image_path_label)
            image_layout.addWidget(btn_image)
            layout.addLayout(image_layout)

            btn_mesh = QPushButton("🚀 Mesh aus Bild erzeugen")
            btn_mesh.clicked.connect(self.handle_mesh)
            layout.addWidget(btn_mesh)

            self.status_label = QLabel("")
            layout.addWidget(self.status_label)

            self.setLayout(layout)
            log.info("[AIPromptPanel][__init__] ✅ Panel initialisiert.")
        except Exception as e:
            log.error(f"[AIPromptPanel][__init__] ❌ Fehler beim Initialisieren: {e}")
            raise

    def handle_generate(self):
        try:
            prompt = self.text_input.toPlainText().strip()
            if not prompt:
                self.text_output.setPlainText("⚠️ Kein Prompt eingegeben.")
                return

            log.info(f"[AIPromptPanel][handle_generate] ▶️ Prompt empfangen: {prompt}")
            result = self.generator.generate_code(prompt)
            self.text_output.setPlainText(result or "⚠️ Keine Antwort erhalten.")
            log.info("[AIPromptPanel][handle_generate] ✅ Code generiert.")
        except Exception as e:
            log.error(f"[AIPromptPanel][handle_generate] ❌ Fehler: {e}")
            self.text_output.setPlainText(f"❌ Fehler: {e}")

    def handle_image(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "", "Bilder (*.png *.jpg *.jpeg)")
            if path:
                self.selected_image_path = path
                self.image_path_label.setText(os.path.basename(path))
                self.generator.set_image_path(path)
                log.info(f"[AIPromptPanel][handle_image] ✅ Bild gewählt: {path}")
                self.status_label.setText("📸 Bild ausgewählt.")
            else:
                self.status_label.setText("⚠️ Kein Bild ausgewählt.")
        except Exception as e:
            log.error(f"[AIPromptPanel][handle_image] ❌ Fehler: {e}")
            self.status_label.setText(f"❌ Fehler: {e}")

    def handle_mesh(self):
        try:
            if not self.selected_image_path:
                self.status_label.setText("⚠️ Bitte zuerst ein Bild auswählen.")
                return

            self.status_label.setText("🌀 Erzeuge Mesh...")
            self.repaint()

            result_path = self.generator.generate_mesh_from_image()
            if result_path and os.path.exists(result_path):
                self.character_system.viewport_ref.load_preview(result_path)
                self.status_label.setText(f"✅ Mesh geladen: {os.path.basename(result_path)}")
                log.success(f"[AIPromptPanel] ✅ Mesh erfolgreich geladen: {result_path}")
            else:
                self.status_label.setText("❌ Keine Mesh-Datei erzeugt.")
                log.error("[AIPromptPanel] ❌ TripoSR hat keine Datei geliefert.")
        except Exception as e:
            log.error(f"[AIPromptPanel][handle_mesh] ❌ Fehler: {e}")
            self.status_label.setText(f"❌ Fehler: {e}")
