from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from ai_backend.triposr_handler import TripoSRHandler

class AIPromptPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Kein Bild ausgewählt.")
        self.select_btn = QPushButton("Bild auswählen")
        self.generate_btn = QPushButton("3D-Modell generieren")

        layout.addWidget(self.label)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.generate_btn)

        self.select_btn.clicked.connect(self.select_image)
        self.generate_btn.clicked.connect(self.generate_mesh)

        self.selected_image = None
        self.setLayout(layout)

    def select_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Bild wählen", "", "Bilder (*.png *.jpg)")
        if file:
            self.selected_image = file
            self.label.setText(f"Bild: {file}")

    def generate_mesh(self):
        if self.selected_image:
            handler = TripoSRHandler()
            handler.run_triposr(self.selected_image)
        else:
            print("Kein Bild ausgewählt.")

