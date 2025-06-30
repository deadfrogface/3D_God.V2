from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt

class NSFWPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("🔞 NSFW-Kontrollen")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.breasts_checkbox = QCheckBox("👙 Brüste anzeigen")
        self.breasts_checkbox.setChecked(True)
        self.breasts_checkbox.stateChanged.connect(self.toggle_breasts)
        layout.addWidget(self.breasts_checkbox)

        self.genital_checkbox = QCheckBox("🍆 Genitalien anzeigen")
        self.genital_checkbox.setChecked(True)
        self.genital_checkbox.stateChanged.connect(self.toggle_genitals)
        layout.addWidget(self.genital_checkbox)

        self.body_hair_checkbox = QCheckBox("🧬 Körperbehaarung")
        self.body_hair_checkbox.setChecked(False)
        self.body_hair_checkbox.stateChanged.connect(self.toggle_bodyhair)
        layout.addWidget(self.body_hair_checkbox)

        self.setLayout(layout)

    def toggle_breasts(self, state):
        self.character_system.anatomy_state["breasts"] = (state == Qt.Checked)
        print(f"👙 Brüste: {'sichtbar' if state else 'ausgeblendet'}")

    def toggle_genitals(self, state):
        self.character_system.anatomy_state["genitals"] = (state == Qt.Checked)
        print(f"🍆 Genitalien: {'sichtbar' if state else 'ausgeblendet'}")

    def toggle_bodyhair(self, state):
        self.character_system.anatomy_state["bodyhair"] = (state == Qt.Checked)
        print(f"🧬 Körperbehaarung: {'an' if state else 'aus'}")