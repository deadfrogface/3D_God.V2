from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
import sys

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.capture_stdout()

    def init_ui(self):
        layout = QVBoxLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        clear_btn = QPushButton("🧹 Konsole leeren")
        clear_btn.clicked.connect(self.clear_console)
        layout.addWidget(clear_btn)

        self.setLayout(layout)

    def capture_stdout(self):
        sys.stdout = self
        sys.stderr = self

    def write(self, msg):
        self.console_output.moveCursor(self.console_output.textCursor().End)
        self.console_output.insertPlainText(msg)

    def flush(self):
        pass

    def clear_console(self):
        self.console_output.clear()