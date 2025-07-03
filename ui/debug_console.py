import sys
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

class DebugConsole(QWidget):
    def __init__(self):
        print("[DebugConsole][__init__] ▶️ Initialisiere Debug-Konsole...")
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
        print("[DebugConsole][__init__] ✅ stdout und stderr umgeleitet")

    def write(self, msg):
        if not msg.strip():
            return
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(msg)
        self.output.moveCursor(QTextCursor.End)

    def flush(self):
        pass  # notwendig für stdout-kompatibilität