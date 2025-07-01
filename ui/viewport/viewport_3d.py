from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtGui import QPixmap
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

    def update_preview(self, layer_state=None):
        if not layer_state:
            self.label.setPixmap(QPixmap())
            self.label.setText("3D-Vorschau hier")
            return

        # Dummy-Logik: Lade passendes Bild (Layer-Kombination als Dateiname)
        key = "_".join([k for k, v in layer_state.items() if v])
        file_path = f"assets/view_preview/{key}.png"

        if os.path.exists(file_path):
            pixmap = QPixmap(file_path).scaled(800, 800, Qt.KeepAspectRatio)
            self.label.setPixmap(pixmap)
            self.label.setText("")
        else:
            self.label.setPixmap(QPixmap())
            self.label.setText("Kein Vorschaubild für:\n" + key)