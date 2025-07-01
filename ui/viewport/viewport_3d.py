from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import os

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.view = QWebEngineView()

        html_path = os.path.abspath("ui/viewport/preview.html")
        self.view.load(QUrl.fromLocalFile(html_path))

        layout.addWidget(self.view)
        self.setLayout(layout)

    def update_preview(self, anatomy_state, asset_state):
        print("[Viewport3D] Preview aktualisiert.")

    def load_animation(self, name):
        print(f"[Viewport3D] Animation geladen: {name}")

    def stop_animation(self):
        print("[Viewport3D] Animation gestoppt.")

    def reload_model(self):
        print("[Viewport3D] Modell-Reload aus GUI")
        self.view.page().runJavaScript("reloadModel('exports/preview.glb')")