from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from core.character_system.character_system import CharacterSystem
from core.logger import log

class AIPanel(QWidget):
    def __init__(self, character_system: CharacterSystem):
        try:
            super().__init__()
            self.character_system = character_system
            layout = QVBoxLayout()

            layout.addWidget(QLabel("🧠 AI Morph Generator"))

            self.prompt_input = QLineEdit()
            self.prompt_input.setPlaceholderText("Optionaler Prompt (z. B. 'muscular warrior')")
            layout.addWidget(self.prompt_input)

            btn = QPushButton("⚡ Erzeuge Morph")
            btn.clicked.connect(self.generate)
            layout.addWidget(btn)

            self.setLayout(layout)
            log.info("[AIPanel][__init__] ✅ Initialisiert")
        except Exception as e:
            log.error(f"[AIPanel][__init__] ❌ Fehler beim Initialisieren: {e}")
            raise

    def generate(self):
        prompt = self.prompt_input.text().strip()
        log.info(f"[AIPanel][generate] ▶️ Starte Morph mit Prompt: '{prompt or '–'}'")
        self.character_system.generate_ai_morph(prompt if prompt else None)
