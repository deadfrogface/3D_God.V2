from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt

class AnatomyViewer(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

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
        self.setLayout(layout)

    def set_layer(self, name, state):
        active = (state == Qt.Checked)
        self.character_system.anatomy_state[name.lower()] = active
        print(f"🧠 Anatomie-Layer '{name}': {'Ein' if active else 'Aus'}")