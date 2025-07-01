from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from core.character_system.character_system import CharacterSystem

class CharacterEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        self.sliders = {
            "height": self.create_slider("Größe", "height"),
            "breast_size": self.create_slider("Brustgröße", "breast_size"),
            "hip_width": self.create_slider("Hüfte", "hip_width"),
            "arm_length": self.create_slider("Armlänge", "arm_length"),
            "leg_length": self.create_slider("Beinlänge", "leg_length")
        }

        for slider in self.sliders.values():
            layout.addLayout(slider["layout"])

        self.setLayout(layout)

    def create_slider(self, label_text, key):
        label = QLabel(label_text)
        slider = QSlider()
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(int(self.character_system.sculpt_data.get(key, 50)))
        slider.valueChanged.connect(lambda val, k=key: self.character_system.update_sculpt_value(k, val))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(slider)
        return {"layout": layout, "slider": slider}
