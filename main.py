import sys
import os
import json
from PySide6.QtWidgets import QApplication
from ui.gui_main_window import MainWindow
from PySide6.QtCore import QTimer

CONFIG_PATH = "config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {
            "theme": "dark",
            "nsfw_enabled": True,
            "controller_enabled": True
        }
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def start_app():
    config = load_config()
    app = QApplication(sys.argv)
    splash = MainWindow(config)
    splash.show()
    QTimer.singleShot(3000, splash.launch_main_gui)
    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()
