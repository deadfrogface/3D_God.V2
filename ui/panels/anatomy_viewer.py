from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from core.character_system.character_system import CharacterSystem

class AnatomyViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🧬 Anatomie-Layer"))

        self.checkboxes = {}
        for layer in ["skin", "fat", "muscle", "bone", "organs"]:
            cb = QCheckBox(f"{layer.capitalize()} anzeigen")
            cb.setChecked(self.character_system.anatomy_state.get(layer, False))
            cb.stateChanged.connect(self.on_checkbox_toggle)
            layout.addWidget(cb)
            self.checkboxes[layer] = cb

        self.setLayout(layout)

    def on_checkbox_toggle(self):
        for layer, cb in self.checkboxes.items():
            state = cb.isChecked()
            self.character_system.update_anatomy_layer(layer, state)