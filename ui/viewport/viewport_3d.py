from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
import os

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.preview_frame = QFrame()
        self.preview_frame.setStyleSheet("background-color: #222; border: 1px solid #555;")
        self.preview_frame.setFixedSize(800, 800)

        self.label = QLabel("3D-Vorschau hier")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #777; font-size: 16pt;")

        layout.addWidget(self.preview_frame)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_preview(self, layer_state=None, asset_state=None):
        if not layer_state:
            self.label.setPixmap(QPixmap())
            self.label.setText("3D-Vorschau hier")
            return

        # Basis-Bild aus Anatomie
        key = "_".join([k for k, v in layer_state.items() if v])
        base_path = f"assets/view_preview/{key}.png"

        if not os.path.exists(base_path):
            self.label.setPixmap(QPixmap())
            self.label.setText("Kein Vorschaubild für:\n" + key)
            return

        base = QPixmap(base_path).scaled(800, 800, Qt.KeepAspectRatio)
        painter = QPainter(base)

        # Überlagerung aller geladenen Assets
        if asset_state:
            for category, items in asset_state.items():
                for item in items:
                    overlay_path = f"assets/view_overlay/{category}/{item}.png"
                    if os.path.exists(overlay_path):
                        overlay = QPixmap(overlay_path).scaled(800, 800, Qt.KeepAspectRatio)
                        painter.drawPixmap(0, 0, overlay)

        painter.end()
        self.label.setPixmap(base)
        self.label.setText("")

def update_preview_from_image(self, image_path):
        pixmap = QPixmap(image_path).scaled(800, 800, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setText("")