from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QHBoxLayout
from core.ai_generation.ai_generator import AIGenerator
from core.logger import log

class AIPromptPanel(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.generator = AIGenerator()
            layout = QVBoxLayout()

            log.info("[AIPromptPanel][__init__] ▶️ Initialisiere AI-Prompt-Panel...")

            layout.addWidget(QLabel("🧠 Text → Code (FauxPilot)"))
            self.text_input = QTextEdit()
            self.text_input.setPlaceholderText("Was soll die KI schreiben? (z. B. Blender-Skript, Material...)")
            layout.addWidget(self.text_input)

            self.text_output = QTextEdit()
            self.text_output.setReadOnly(True)
            layout.addWidget(self.text_output)

            btn_generate = QPushButton("Code generieren")
            btn_generate.clicked.connect(self.handle_generate)
            layout.addWidget(btn_generate)

            layout.addWidget(QLabel("🖼️ Bild → Mesh (TripoSR)"))
            image_layout = QHBoxLayout()
            self.image_path_label = QLabel("Kein Bild gewählt")
            btn_image = QPushButton("Bild laden")
            btn_image.clicked.connect(self.handle_image)
            image_layout.addWidget(self.image_path_label)
            image_layout.addWidget(btn_image)
            layout.addLayout(image_layout)

            btn_mesh = QPushButton("Mesh aus Bild erzeugen")
            btn_mesh.clicked.connect(self.handle_mesh)
            layout.addWidget(btn_mesh)

            layout.addWidget(QLabel("💪 AI-Körperform (CharMorph):"))
            self.charmorph_input = QTextEdit()
            self.charmorph_input.setPlaceholderText("z. B. 'slim tall male', 'muscular orc woman'")
            layout.addWidget(self.charmorph_input)

            btn_shape = QPushButton("Körperform generieren")
            btn_shape.clicked.connect(self.handle_shape)
            layout.addWidget(btn_shape)

            self.setLayout(layout)
            log.info("[AIPromptPanel][__init__] ✅ Panel bereit")
        except Exception as e:
            log.error(f"[AIPromptPanel][__init__] ❌ Fehler bei der Initialisierung: {e}")
            raise

    def handle_generate(self):
        prompt = self.text_input.toPlainText()
        log.info(f"[AIPromptPanel][handle_generate] ▶️ Prompt empfangen: {prompt}")
        result = self.generator.generate_code(prompt)
        self.text_output.setPlainText(result)
        log.info("[AIPromptPanel][handle_generate] ✅ Code generiert")

    def handle_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "", "Bilder (*.png *.jpg *.jpeg)")
        if path:
            self.image_path_label.setText(path)
            self.generator.set_image_path(path)
            log.info(f"[AIPromptPanel][handle_image] 📷 Bild gesetzt: {path}")
        else:
            log.warning("[AIPromptPanel][handle_image] ❌ Kein Bild gewählt")

    def handle_mesh(self):
        log.info("[AIPromptPanel][handle_mesh] ▶️ Starte Mesh-Generierung via TripoSR")
        self.generator.generate_mesh_from_image()
        log.info("[AIPromptPanel][handle_mesh] ✅ Vorgang abgeschlossen")

    def handle_shape(self):
        prompt = self.charmorph_input.toPlainText()
        log.info(f"[AIPromptPanel][handle_shape] ▶️ Prompt für Morphing: {prompt}")
        shape = self.generator.generate_shape_from_prompt(prompt)
        if shape:
            for key, value in shape.items():
                self.generator.character_system.update_sculpt_value(key, value)
                log.info(f"[AIPromptPanel][handle_shape] 🔁 {key} = {value}")
            log.info("[AIPromptPanel][handle_shape] ✅ Körperform übernommen")
        else:
            log.warning("[AIPromptPanel][handle_shape] ❌ Keine gültige Form empfangen")
