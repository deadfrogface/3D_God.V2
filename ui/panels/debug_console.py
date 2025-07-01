from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import sys

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.console_output)
        self.setLayout(layout)

        sys.stdout = self
        sys.stderr = self

    def write(self, message):
        self.console_output.moveCursor(self.console_output.textCursor().End)
        self.console_output.insertPlainText(message)

    def flush(self):
        pass