from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QFileDialog
)
import sys
import os
import datetime
import re
from core.logger import log


class DebugConsole(QWidget):
    def __init__(self):
        try:
            super().__init__()
            log.info("[DebugConsole][__init__] ▶️ Initialisiere Debug-Konsole...")
            self.setWindowTitle("🛠 Debug-Konsole")
            layout = QVBoxLayout()

            self.filters = {
                "Sculpt": QCheckBox("Sculpt"),
                "Export": QCheckBox("Export"),
                "Rig": QCheckBox("Rig"),
                "AI": QCheckBox("AI"),
                "All": QCheckBox("Alle anzeigen")
            }
            filter_row = QHBoxLayout()
            for cb in self.filters.values():
                cb.setChecked(False)
                cb.stateChanged.connect(self.apply_filter)  # ✅ Methode ist jetzt definiert
                filter_row.addWidget(cb)
            layout.addLayout(filter_row)

            self.search_box = QLineEdit()
            self.search_box.setPlaceholderText("🔍 Suche im Log...")
            self.search_box.textChanged.connect(self.apply_filter)
            layout.addWidget(self.search_box)

            self.output = QTextEdit()
            self.output.setReadOnly(True)
            layout.addWidget(self.output)

            btn_row = QHBoxLayout()
            btn_clear = QPushButton("🧹 Leeren")
            btn_clear.clicked.connect(self.clear_console)
            btn_row.addWidget(btn_clear)

            btn_export = QPushButton("📁 Log exportieren")
            btn_export.clicked.connect(self.export_log)
            btn_row.addWidget(btn_export)
            layout.addLayout(btn_row)

            btn_diagnostics = QPushButton("🧠 Projekt-Diagnose starten")
            btn_diagnostics.clicked.connect(self.run_diagnostics)
            layout.addWidget(btn_diagnostics)

            self.setLayout(layout)
            self.full_log = []

            sys.stdout = self
            sys.stderr = self
            log.info("[DebugConsole][__init__] ✅ Debug-Konsole bereit.")
        except Exception as e:
            log.error(f"[DebugConsole][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def apply_filter(self):
        self.output.clear()
        search = self.search_box.text().lower()
        count = 0
        for line in self.full_log:
            if self._passes_filter(line) and search in line.lower():
                self.output.append(line)
                count += 1
        log.debug(f"[DebugConsole][apply_filter] ✅ {count} Zeilen angezeigt")

    def _passes_filter(self, msg):
        if self.filters["All"].isChecked():
            return True
        for key, cb in self.filters.items():
            if cb.isChecked() and key.lower() in msg.lower():
                return True
        return False

    def clear_console(self):
        self.full_log.clear()
        self.output.clear()
        log.info("[DebugConsole][clear_console] ✅ Konsole geleert")

    def export_log(self):
        path, _ = QFileDialog.getSaveFileName(self, "Speichere Log als", "debug_log.txt", "Textdateien (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.full_log))
            log.info(f"[DebugConsole][export_log] ✅ Log gespeichert: {path}")
        else:
            log.warning("[DebugConsole][export_log] ❌ Kein Pfad gewählt")

    def run_diagnostics(self):
        log.info("[DebugConsole][run_diagnostics] ▶️ Starte Projektprüfung...")
        # ... hier käme deine bestehende Diagnoselogik ...
