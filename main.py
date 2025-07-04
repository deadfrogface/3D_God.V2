import sys
import os
import json
import traceback
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from ui.gui_main_window import MainWindow
from core.logger import log

CONFIG_PATH = "config.json"

def load_config():
    log.info("Lade Konfiguration...")
    if not os.path.exists(CONFIG_PATH):
        log.info("Keine config.json gefunden – verwende Standardwerte")
        return {
            "theme": "dark",
            "nsfw_enabled": True,
            "controller_enabled": True
        }
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            log.info("Konfiguration erfolgreich geladen.")
            return config
    except Exception as e:
        log.error(f"Fehler beim Laden der Konfiguration: {e}")
        return {
            "theme": "dark",
            "nsfw_enabled": True,
            "controller_enabled": True
        }

def save_config(config):
    log.info("Speichere Konfiguration...")
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        log.info("Konfiguration gespeichert.")
    except Exception as e:
        log.error(f"Fehler beim Speichern der Konfiguration: {e}")

def start_app():
    try:
        log.info("Starte GUI-Anwendung...")
        config = load_config()

        app = QApplication(sys.argv)
        log.info("Initialisiere MainWindow mit geladener Konfiguration...")
        splash = MainWindow(config)

        log.info("Zeige Hauptfenster...")
        splash.show()

        log.info("Starte zeitverzögerte GUI-Initialisierung (3s)...")
        QTimer.singleShot(3000, splash.launch_main_gui)

        log.info("GUI bereit – Starte Event Loop")
        sys.exit(app.exec())

    except Exception as e:
        log.error(f"❌ Schwerwiegender Fehler beim Start: {e}")
        tb = traceback.format_exc()
        log.error(tb)
        sys.exit(1)

if __name__ == "__main__":
    start_app()
