import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QHBoxLayout, QSpinBox, QLabel, QMessageBox
)

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "froggy_memory.json")

class MemoryEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐸 Froggy Memory Editor")
        self.setGeometry(200, 200, 600, 400)
        self.memory = self.load_memory()

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.refresh_list()
        layout.addWidget(self.list)

        control_layout = QHBoxLayout()
        self.label_spin = QSpinBox()
        self.label_spin.setMinimum(0)
        self.label_spin.setMaximum(99)
        control_layout.addWidget(QLabel("Label ändern zu:"))
        control_layout.addWidget(self.label_spin)

        btn_update = QPushButton("✅ Label speichern")
        btn_update.clicked.connect(self.update_label)
        control_layout.addWidget(btn_update)

        btn_delete = QPushButton("🗑️ Eintrag löschen")
        btn_delete.clicked.connect(self.delete_entry)
        control_layout.addWidget(btn_delete)

        layout.addLayout(control_layout)
        self.setLayout(layout)

    def load_memory(self):
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def refresh_list(self):
        self.list.clear()
        for idx, entry in enumerate(self.memory):
            self.list.addItem(f"#{idx} → x={entry['x']} | y={entry['y']}")

    def update_label(self):
        current = self.list.currentRow()
        if current < 0:
            QMessageBox.warning(self, "❌ Fehler", "Bitte Eintrag auswählen.")
            return
        new_label = self.label_spin.value()
        self.memory[current]["y"] = new_label
        self.save_memory()
        self.refresh_list()

    def delete_entry(self):
        current = self.list.currentRow()
        if current < 0:
            QMessageBox.warning(self, "❌ Fehler", "Bitte Eintrag auswählen.")
            return
        confirm = QMessageBox.question(self, "Löschen?", "Diesen Eintrag wirklich löschen?")
        if confirm == QMessageBox.Yes:
            self.memory.pop(current)
            self.save_memory()
            self.refresh_list()

    def save_memory(self):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MemoryEditor()
    win.show()
    sys.exit(app.exec())