from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt

class CharacterEditorPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.sliders = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🧍 Körperform & Proportionen")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        for label, key in [
            ("Größe", "height"),
            ("Brustgröße", "chest_size"),
            ("Hüfte", "hip_width"),
            ("Armlänge", "arm_length"),
            ("Beinlänge", "leg_length")
        ]:
            box = self.create_slider(label, key)
            layout.addLayout(box)

        layout.addStretch()
        self.setLayout(layout)

    def create_slider(self, name, key):
        layout = QHBoxLayout()
        label = QLabel(name)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(50, 150)
        slider.setValue(100)
        slider.valueChanged.connect(lambda val, k=key: self.update_value(k, val / 100))
        layout.addWidget(label)
        layout.addWidget(slider)
        self.sliders[key] = slider
        return layout

    def update_value(self, key, value):
        self.character_system.sculpt_data[key] = value
        print(f"🔧 {key}: {value}")