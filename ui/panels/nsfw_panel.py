from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt

class NSFWPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()
        self.character_system.nsfw_sync_callback = self.update_nsfw_checkboxes

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("🔞 NSFW-Kontrollen")
        layout.addWidget(label)

        self.breasts_checkbox = QCheckBox("👙 Brüste anzeigen")
        self.breasts_checkbox.setChecked(self.character_system.anatomy_state.get("breasts", True))
        self.breasts_checkbox.stateChanged.connect(self.toggle_breasts)
        layout.addWidget(self.breasts_checkbox)

        self.genital_checkbox = QCheckBox("🍆 Genitalien anzeigen")
        self.genital_checkbox.setChecked(self.character_system.anatomy_state.get("genitals", True))
        self.genital_checkbox.stateChanged.connect(self.toggle_genitals)
        layout.addWidget(self.genital_checkbox)

        self.body_hair_checkbox = QCheckBox("🧬 Körperbehaarung")
        self.body_hair_checkbox.setChecked(self.character_system.anatomy_state.get("bodyhair", False))
        self.body_hair_checkbox.stateChanged.connect(self.toggle_bodyhair)
        layout.addWidget(self.body_hair_checkbox)

        self.setLayout(layout)

    def toggle_breasts(self, state):
        self.character_system.anatomy_state["breasts"] = (state == Qt.Checked)
        self.character_system.refresh_layers()

    def toggle_genitals(self, state):
        self.character_system.anatomy_state["genitals"] = (state == Qt.Checked)
        self.character_system.refresh_layers()

    def toggle_bodyhair(self, state):
        self.character_system.anatomy_state["bodyhair"] = (state == Qt.Checked)
        self.character_system.refresh_layers()

    def update_nsfw_checkboxes(self):
        self.breasts_checkbox.setChecked(self.character_system.anatomy_state.get("breasts", True))
        self.genital_checkbox.setChecked(self.character_system.anatomy_state.get("genitals", True))
        self.body_hair_checkbox.setChecked(self.character_system.anatomy_state.get("bodyhair", False))