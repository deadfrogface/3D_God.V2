from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
import os

class Viewport3D(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.character_system.bind_viewport(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🖼️ 3D Vorschau")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ➕ Platzhalter-Rahmen (optional für späteren OpenGL- oder Qt3D-Ersatz)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #222; border: 2px dashed #00ff88;")
        self.frame.setMinimumHeight(400)
        layout.addWidget(self.frame)

        # 📷 Pixmap-Vorschau (z. B. als gerendertes Blender-Bild)
        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(300, 300)
        pixmap.fill(Qt.black)
        self.preview.setPixmap(pixmap)
        layout.addWidget(self.preview)

        layout.addStretch()
        self.setLayout(layout)

    def update_view(self):
        preview_path = "exports/preview.png"
        if os.path.exists(preview_path):
            image = QImage(preview_path)
            self.preview.setPixmap(QPixmap.fromImage(image).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            print(f"🖼️ Vorschau geladen: {preview_path}")
        else:
            print(f"❌ Keine Vorschau gefunden: {preview_path}")