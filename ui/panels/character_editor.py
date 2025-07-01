from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt
from core.character_system.character_system import CharacterSystem

class CharacterEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🧍‍♂️ Körperform-Editor"))

        self.sliders = {}

        # Definiere alle Sculpt-Parameter mit Name, Bereich, Startwert
        fields = {
            "height":        ("Größe",       0, 100),
            "breast_size":   ("Brustgröße",  0, 100),
            "hip_width":     ("Hüften",      0, 100),
            "arm_length":    ("Armlänge",    0, 100),
            "leg_length":    ("Beinlänge",   0, 100),
        }

        for key, (label, min_val, max_val) in fields.items():
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(self.character_system.sculpt_data.get(key, 50))
            slider.valueChanged.connect(lambda val, k=key: self.update_value(k, val))
            self.sliders[key] = slider
            row.addWidget(slider)
            layout.addLayout(row)

        self.setLayout(layout)

    def update_value(self, key, value):
        self.character_system.update_sculpt_value(key, value)