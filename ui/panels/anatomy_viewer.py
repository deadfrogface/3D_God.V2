from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QTextEdit, QPushButton
from PySide6.QtCore import Qt

class AnatomyViewer(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()
        self.character_system.anatomy_panel = self  # Rückbindung

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("🧠 Anatomie-Layer")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.checkboxes = {}
        for layer in ["Haut", "Fett", "Muskeln", "Knochen", "Organe"]:
            checkbox = QCheckBox(layer)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, l=layer: self.set_layer(l, state))
            layout.addWidget(checkbox)
            self.checkboxes[layer.lower()] = checkbox

        layout.addStretch()
        layout.addWidget(QLabel("🪵 Debug-Konsole"))
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        clear_btn = QPushButton("🧹 Leeren")
        clear_btn.clicked.connect(self.clear_console)
        layout.addWidget(clear_btn)

        self.setLayout(layout)

    def set_layer(self, name, state):
        active = (state == Qt.Checked)
        self.character_system.update_anatomy_layer(name, active)
        self.character_system.refresh_layers()

    def update_checkboxes(self):
        for layer, checkbox in self.checkboxes.items():
            state = self.character_system.anatomy_state.get(layer, True)
            checkbox.setChecked(state)

    def log(self, message):
        self.console_output.append(message)

    def clear_console(self):
        self.console_output.clear()