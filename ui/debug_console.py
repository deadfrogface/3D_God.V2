import sys
from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

class DebugConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Debug-Konsole")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)
        self.setLayout(layout)

        # Umleitung des stdout/stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, text):
        self.output_box.moveCursor(self.output_box.textCursor().End)
        self.output_box.insertPlainText(text)

    def flush(self):
        pass  # notwendig für Kompatibilität mit `print()`

    def toggle(self):
        self.setVisible(not self.isVisible())