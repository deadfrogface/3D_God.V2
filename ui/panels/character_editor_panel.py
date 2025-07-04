from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCore import Qt
from core.logger import log

class CharacterEditorPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.character_system.slider_sync_callback = self.refresh_sliders

        log.info("[CharacterEditorPanel][__init__] ▶️ Initialisiere Körperform-Editor")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🧍‍♂️ Körperform-Editor"))

        self.sliders = {}
        self.fields = {
            "height":      ("Größe",       0, 100),
            "breast_size": ("Brustgröße",  0, 100),
            "hip_width":   ("Hüften",      0, 100),
            "arm_length":  ("Armlänge",    0, 100),
            "leg_length":  ("Beinlänge",   0, 100)
        }

        for key, (label, min_val, max_val) in self.fields.items():
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
        log.info("[CharacterEditorPanel][__init__] ✅ Initialisierung abgeschlossen")

    def update_value(self, key, value):
        log.debug(f"[CharacterEditorPanel][update_value] 🔧 {key} → {value}")
        self.character_system.update_sculpt_value(key, value)

    def refresh_sliders(self):
        log.debug("[CharacterEditorPanel][refresh_sliders] 🔄 Synchronisiere Slider")
        for key, slider in self.sliders.items():
            new_val = self.character_system.sculpt_data.get(key, 50)
            if slider.value() != new_val:
                slider.setValue(new_val)
