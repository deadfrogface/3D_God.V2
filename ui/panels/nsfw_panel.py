from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class NSFWPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        layout = QVBoxLayout()

        label = QLabel("🔞 NSFW Optionen")
        layout.addWidget(label)

        toggle_btn = QPushButton("Sichtbarkeit umschalten")
        toggle_btn.clicked.connect(self.toggle)

        layout.addWidget(toggle_btn)
        self.setLayout(layout)

    def toggle(self):
        current = self.character_system.is_nsfw()
        self.character_system.set_nsfw_mode(not current)
