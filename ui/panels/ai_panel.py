from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from core.character_system.character_system import CharacterSystem

class AIPanel(QWidget):
    def __init__(self, character_system: CharacterSystem):
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

    def generate(self):
        prompt = self.prompt_input.text().strip()
        self.character_system.generate_ai_morph(prompt if prompt else None)