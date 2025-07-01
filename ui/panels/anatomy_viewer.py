from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from core.character_system.character_system import CharacterSystem

class NSFWPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.breasts_cb = QCheckBox("Brüste anzeigen")
        self.genitals_cb = QCheckBox("Genitalien anzeigen")
        self.bodyhair_cb = QCheckBox("Körperbehaarung anzeigen")

        self.breasts_cb.setChecked(self.character_system.anatomy_state.get("breasts", True))
        self.genitals_cb.setChecked(self.character_system.anatomy_state.get("genitals", True))
        self.bodyhair_cb.setChecked(self.character_system.anatomy_state.get("bodyhair", False))

        self.breasts_cb.stateChanged.connect(lambda state: self.toggle("breasts", state))
        self.genitals_cb.stateChanged.connect(lambda state: self.toggle("genitals", state))
        self.bodyhair_cb.stateChanged.connect(lambda state: self.toggle("bodyhair", state))

        layout.addWidget(self.breasts_cb)
        layout.addWidget(self.genitals_cb)
        layout.addWidget(self.bodyhair_cb)
        self.setLayout(layout)

    def toggle(self, key, state):
        self.character_system.update_anatomy_layer(key, state == 2)
        self.character_system.refresh_layers()