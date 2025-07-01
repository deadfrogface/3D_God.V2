from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt
from core.character_system.character_system import CharacterSystem

class CharacterEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📏 Körperform & Proportionen"))

        self.sliders = {}
        fields = {
            "height": "Größe",
            "breast_size": "Brustgröße",
            "hip_width": "Hüfte",
            "arm_length": "Arme",
            "leg_length": "Beine"
        }

        for key, label in fields.items():
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(label))
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(self.character_system.sculpt_data.get(key, 50))
            slider.valueChanged.connect(lambda val, k=key: self.update_slider(k, val))
            hlayout.addWidget(slider)
            layout.addLayout(hlayout)
            self.sliders[key] = slider

        self.setLayout(layout)

    def update_slider(self, key, value):
        self.character_system.update_sculpt_value(key, value)