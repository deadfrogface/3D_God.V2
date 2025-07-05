import sys
import os
import datetime
import re
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton,
    QHBoxLayout, QCheckBox, QLineEdit, QFileDialog
)
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
                cb.stateChanged.connect(self.apply_filter)
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
