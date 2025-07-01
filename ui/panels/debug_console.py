from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QCheckBox, QLineEdit, QFileDialog
import sys
import datetime

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛠 Debug-Konsole")
        layout = QVBoxLayout()

        # Filter-Kategorien
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

        # Suchfeld
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Suche im Log...")
        self.search_box.textChanged.connect(self.apply_filter)
        layout.addWidget(self.search_box)

        # Textausgabe
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Buttons
        btn_row = QHBoxLayout()
        btn_clear = QPushButton("🧹 Leeren")
        btn_clear.clicked.connect(self.clear_console)
        btn_row.addWidget(btn_clear)

        btn_export = QPushButton("📁 Log exportieren")
        btn_export.clicked.connect(self.export_log)
        btn_row.addWidget(btn_export)

        layout.addLayout(btn_row)
        self.setLayout(layout)

        self.full_log = []
        sys.stdout = self

    def write(self, message):
        msg = message.strip()
        if msg:
            timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
            log_entry = f"{timestamp} {msg}"
            self.full_log.append(log_entry)
            self.apply_filter()

    def flush(self):
        pass

    def apply_filter(self):
        self.output.clear()
        search = self.search_box.text().lower()
        for line in self.full_log:
            if self._passes_filter(line) and search in line.lower():
                self.output.append(line)

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

    def export_log(self):
        path, _ = QFileDialog.getSaveFileName(self, "Speichere Log als", "debug_log.txt", "Textdateien (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.full_log))