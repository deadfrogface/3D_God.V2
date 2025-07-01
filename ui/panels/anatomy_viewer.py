from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QTextEdit, QLabel
from core.character_system.character_system import CharacterSystem

class AnatomyViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        self.checkboxes = {}

        layout = QVBoxLayout()
        label = QLabel("Körperschichten anzeigen:")
        layout.addWidget(label)

        for layer in ["skin", "fat", "muscle", "bone", "organs"]:
            checkbox = QCheckBox(layer.capitalize())
            checkbox.setChecked(self.character_system.anatomy_state.get(layer, False))
            checkbox.stateChanged.connect(lambda state, l=layer: self.set_layer(l, state == 2))
            layout.addWidget(checkbox)
            self.checkboxes[layer] = checkbox

        self.debug_log = QTextEdit()
        self.debug_log.setReadOnly(True)
        layout.addWidget(self.debug_log)

        self.setLayout(layout)

    def set_layer(self, layer_name, state):
        self.character_system.update_anatomy_layer(layer_name, state)
        self.debug_log.append(f"[Anatomie] {layer_name}: {'✔️' if state else '❌'}")
        self.character_system.refresh_layers()