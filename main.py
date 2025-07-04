import sys
import os
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.gui_main_window import MainWindow
from core.logger import log  # ← Logging aus zentralem Modul

CONFIG_PATH = "config.json"

def load_config():
    log.info("Lade Konfiguration...", "INFO")
    if not os.path.exists(CONFIG_PATH):
        log.info("Keine config.json gefunden – verwende Standardwerte", "INFO")
        return {
            "theme": "dark",
            "nsfw_enabled": True,
            "controller_enabled": True
        }
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            log.info("Konfiguration erfolgreich geladen.", "SUCCESS")
            return config
    except Exception as e:
        log.info(f"Fehler beim Laden der Konfiguration: {e}", "ERROR")
        return {
            "theme": "dark",
            "nsfw_enabled": True,
            "controller_enabled": True
        }

def save_config(config):
    log.info("Speichere Konfiguration...", "INFO")
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        log.info("Konfiguration gespeichert.", "SUCCESS")
    except Exception as e:
        log.info(f"Fehler beim Speichern der Konfiguration: {e}", "ERROR")

def start_app():
    log.info("Starte GUI-Anwendung...")
    config = load_config()
    app = QApplication(sys.argv)
    splash = MainWindow(config)
    splash.show()
    QTimer.singleShot(3000, splash.launch_main_gui)
    log.info("GUI bereit – Starte Event Loop", "SUCCESS")
    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()
