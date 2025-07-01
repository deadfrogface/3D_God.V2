from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QFileInfo, QTimer
import os

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.view = QWebEngineView()

        self.model_path = os.path.abspath("exports/preview.glb")
        self.html_path = os.path.abspath("ui/viewport/preview.html")
        self.view.load(QUrl.fromLocalFile(self.html_path))

        layout.addWidget(self.view)
        self.setLayout(layout)

        # Nach 2s Model neu laden, sobald bereit
        QTimer.singleShot(2000, self.reload_model)

    def reload_model(self):
        print("[Viewport] Neuladen des Modells im Webview...")
        self.view.page().runJavaScript(f"reloadModel('{self.model_path.replace(os.sep, '/')}')")

    def update_preview(self, anatomy_state, asset_state):
        print("[Viewport3D] update_preview → Model bleibt geladen")

    def load_animation(self, name):
        print(f"[Viewport3D] Animation '{name}' (noch nicht angebunden)")

    def stop_animation(self):
        print("[Viewport3D] Animation gestoppt.")