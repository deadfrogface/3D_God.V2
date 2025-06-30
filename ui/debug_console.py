from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import sys

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐞 Debug-Konsole")
        self.resize(800, 300)

        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        self.setLayout(layout)

        # Redirect stdout and stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, text):
        self.output.moveCursor(self.output.textCursor().End)
        self.output.insertPlainText(text)

    def flush(self):
        pass  # Needed for sys.stdout