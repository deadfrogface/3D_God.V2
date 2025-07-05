from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
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
        try:
            prompt = self.prompt_input.text().strip()
            log.info(f"[AIPanel][generate] ▶️ Starte Morph mit Prompt: '{prompt or '–'}'")
            result = self.character_system.generate_ai_morph(prompt if prompt else None)

            if result is None:
                QMessageBox.warning(self, "Fehlgeschlagen", "Die Morph-Generierung hat kein Ergebnis geliefert.")
                log.warning("[AIPanel][generate] ⚠️ Keine Werte von der KI erhalten")
            else:
                QMessageBox.information(self, "Erfolg", "Körperform erfolgreich generiert.")
                log.info("[AIPanel][generate] ✅ Morph erfolgreich übernommen")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Morphing:\n{e}")
            log.error(f"[AIPanel][generate] ❌ Fehler bei Morphing: {e}")
