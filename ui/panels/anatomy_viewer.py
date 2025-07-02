from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from core.character_system.character_system import CharacterSystem

class AnatomyViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🧬 Anatomie-Viewer"))

        self.checkboxes = {}

        for layer in ["skin", "fat", "muscle", "bone", "organs"]:
            checkbox = QCheckBox(layer.capitalize())
            checkbox.setChecked(self.character_system.anatomy_state.get(layer, False))
            checkbox.stateChanged.connect(lambda state, l=layer: self.toggle_layer(l, state))
            layout.addWidget(checkbox)
            self.checkboxes[layer] = checkbox

        self.setLayout(layout)

    def toggle_layer(self, layer, state):
        self.character_system.anatomy_state[layer] = bool(state)
        print(f"[Anatomie] {layer}: {'Aktiv' if state else 'Deaktiviert'}")
        self.character_system.refresh_layers()