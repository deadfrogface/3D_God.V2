from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from core.logger import log
import os

class Viewport3D(QWidget):
    def __init__(self, character_system):
        log.info("[Viewport3D][__init__] ▶️ Initialisiere Viewport...")
        super().__init__()
        self.character_system = character_system
        self.character_system.bind_viewport(self)
        self.init_ui()
        log.info("[Viewport3D][__init__] ✅ Viewport bereit")

    def init_ui(self):
        log.info("[Viewport3D][init_ui] ▶️ Baue UI...")
        layout = QVBoxLayout()

        title = QLabel("🖼️ 3D Vorschau")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #222; border: 2px dashed #00ff88;")
        self.frame.setMinimumHeight(400)
        layout.addWidget(self.frame)

        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(300, 300)
        pixmap.fill(Qt.black)
        self.preview.setPixmap(pixmap)
        layout.addWidget(self.preview)

        layout.addStretch()
        self.setLayout(layout)
        log.info("[Viewport3D][init_ui] ✅ UI aufgebaut")

    def update_view(self):
        log.info("[Viewport3D][update_view] ▶️ Aktualisiere Vorschau...")
        preview_path = "exports/preview.png"
        if os.path.exists(preview_path):
            image = QImage(preview_path)
            pixmap = QPixmap.fromImage(image).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview.setPixmap(pixmap)
            log.info(f"[Viewport3D][update_view] ✅ Vorschau geladen: {preview_path}")
        else:
            log.error(f"[Viewport3D][update_view] ❌ Keine Vorschau gefunden: {preview_path}")

    def update_preview(self, anatomy_state=None, asset_state=None):
        log.info("[Viewport3D][update_preview] 🌀 Aktualisiere 3D-Vorschau (anatomy/assets)")
        # Hier könntest du anatomy_state / asset_state auswerten, falls benötigt
        self.update_view()

    def load_preview(self, path):
        log.info(f"[Viewport3D][load_preview] 📥 Lade Vorschau aus Pfad: {path}")
        if os.path.exists(path):
            image = QImage(path)
            pixmap = QPixmap.fromImage(image).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview.setPixmap(pixmap)
            log.success(f"[Viewport3D][load_preview] ✅ Vorschau geladen")
        else:
            log.error(f"[Viewport3D][load_preview] ❌ Pfad nicht gefunden: {path}")