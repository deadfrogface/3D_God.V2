from PySide6.QtWidgets import QApplication
from core.logger import log  # Zentrales Logging

class StyleManager:
    THEMES = {
        "dark": {
            "stylesheet": """
                QWidget {
                    background-color: #1e1e1e;
                    color: #dddddd;
                    font-family: 'Segoe UI';
                    font-size: 12pt;
                }
                QPushButton {
                    background-color: #2a2a2a;
                    border: 1px solid #555;
                    padding: 6px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """
        },
        "light": {
            "stylesheet": """
                QWidget {
                    background-color: #f0f0f0;
                    color: #222222;
                    font-family: 'Segoe UI';
                    font-size: 12pt;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #aaa;
                    padding: 6px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """
        }
    }

    @staticmethod
    def apply_theme(theme_name: str):
        log(f"[StyleManager][apply_theme] Eingabe: theme = {theme_name}", "INFO")
        try:
            theme = StyleManager.THEMES.get(theme_name, StyleManager.THEMES["dark"])
            QApplication.instance().setStyleSheet(theme["stylesheet"])
            log(f"[StyleManager][apply_theme] Theme '{theme_name}' angewendet", "SUCCESS")
        except Exception as e:
            log(f"[StyleManager][apply_theme] Fehler: {e}", "ERROR")