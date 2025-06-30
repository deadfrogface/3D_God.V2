#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from ui.main_window import MainWindow
from core.character_system.character_system import CharacterSystem
from core.ai_generation.ai_generator import AIGenerator

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_app()
        self.load_config()
        self.show_splash()

    def setup_app(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        self.app.setApplicationName("3D_God")
        self.app.setStyle("Fusion")

    def load_config(self):
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "theme": "cyberpunk",
                "nsfw_enabled": True,
                "controller_enabled": True,
                "blender_path": "blender_embedded/blender_3.6_portable/blender.exe"
            }

    def show_splash(self):
        splash_pix = QPixmap(600, 400)
        splash_pix.fill(Qt.black)

        self.splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        self.splash.setFont(QFont("Arial", 24, QFont.Bold))
        self.splash.show()
        self.splash.showMessage(
            "🔱 3D_God lädt ...",
            Qt.AlignCenter,
            Qt.white
        )

        QTimer.singleShot(100, self.initialize_systems)

    def initialize_systems(self):
        try:
            self.splash.showMessage("🧠 Initialisiere Charaktersystem ...", Qt.AlignCenter, Qt.white)
            self.character_system = CharacterSystem()

            self.splash.showMessage("🤖 Lade KI-Module ...", Qt.AlignCenter, Qt.white)
            self.ai_generator = AIGenerator(self.config)

            self.splash.showMessage("🖥️ Starte Benutzeroberfläche ...", Qt.AlignCenter, Qt.white)
            self.main_window = MainWindow(self.config, self.character_system, self.ai_generator)

            QTimer.singleShot(500, self.show_main_window)

        except Exception as e:
            self.splash.showMessage(f"❌ Fehler: {str(e)}", Qt.AlignCenter, Qt.red)
            QTimer.singleShot(3000, self.app.quit)

    def show_main_window(self):
        self.main_window.show()
        self.splash.finish(self.main_window)

    def run(self):
        return self.app.exec()

def main():
    app = Application()
    sys.exit(app.run())

if __name__ == "__main__":
    main()