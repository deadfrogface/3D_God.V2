import sys
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐞 Debug-Konsole")
        self.resize(800, 400)
        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #111; color: #0f0; font-family: monospace;")
        layout.addWidget(self.output)
        self.setLayout(layout)

        sys.stdout = self
        sys.stderr = self

    def write(self, msg):
        self.output.moveCursor(Qt.TextCursor.End)
        self.output.insertPlainText(msg)

    def flush(self):
        pass  # nötig für stdout-kompatibilität