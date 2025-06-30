from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class Viewport3D(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.character_system.viewport = self  # Rückkanal zur Anzeige

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🖼️ 3D Vorschau")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Placeholder Frame (z. B. für OpenGL- oder Blender-Integration später)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #222; border: 2px dashed #00ff88;")
        self.frame.setMinimumHeight(400)
        layout.addWidget(self.frame)

        # Optional: Bildvorschau
        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(300, 300)
        pixmap.fill(Qt.black)
        self.preview.setPixmap(pixmap)
        layout.addWidget(self.preview)

        layout.addStretch()
        self.setLayout(layout)

    def update_view(self):
        print("🔄 Viewport aktualisieren – Placeholder bleibt")