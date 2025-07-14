# ui/panels/character_editor_panel.py

import os
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from core.logger import log
import os

PARAMS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../assets/body_parameters.json")
)



class CharacterEditorPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.character_system.slider_sync_callback = self.refresh_sliders
        self.sliders = {}

        try:
            log.info("[CharacterEditorPanel][__init__] ▶️ Initialisiere Körperform-Editor")

            layout = QVBoxLayout()
            layout.addWidget(QLabel("🧍‍♂️ Körperform-Editor"))

            # ➕ Gender-Buttons
            gender_row = QHBoxLayout()
            male_btn = QPushButton("♂ Männlich")
            female_btn = QPushButton("♀ Weiblich")
            male_btn.clicked.connect(self.set_male)
            female_btn.clicked.connect(self.set_female)
            gender_row.addWidget(male_btn)
            gender_row.addWidget(female_btn)
            layout.addLayout(gender_row)

            # 🔧 Sliders
            self.fields = self.load_parameters()
            for key, params in self.fields.items():
                label_text = params.get("label", key)
                min_val = params.get("min", 0)
                max_val = params.get("max", 100)
                default_val = self.character_system.sculpt_data.get(key, params.get("default", 50))

                row = QHBoxLayout()
                row.addWidget(QLabel(label_text))

                slider = QSlider(Qt.Horizontal)
                slider.setRange(min_val, max_val)
                slider.setValue(default_val)
                slider.valueChanged.connect(lambda val, k=key: self.on_slider_changed(k, val))

                self.sliders[key] = slider
                row.addWidget(slider)
                layout.addLayout(row)

            self.setLayout(layout)
            log.success("[CharacterEditorPanel][__init__] ✅ Initialisierung abgeschlossen")
        except Exception as e:
            log.error(f"[CharacterEditorPanel][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def load_parameters(self):
        if not os.path.exists(PARAMS_FILE):
            log.error(f"[CharacterEditorPanel][load_parameters] ❌ Datei nicht gefunden: {PARAMS_FILE}")
            return {}

        try:
            with open(PARAMS_FILE, "r", encoding="utf-8") as f:
                params = json.load(f)
                log.success(f"[CharacterEditorPanel][load_parameters] ✅ Parameter geladen: {len(params)}")
                return params
        except Exception as e:
            log.error(f"[CharacterEditorPanel][load_parameters] ❌ Fehler beim Laden: {e}")
            return {}

    def on_slider_changed(self, key, value):
        log.debug(f"[CharacterEditorPanel][on_slider_changed] 🔧 {key} → {value}")
        if self.character_system:
            self.character_system.update_sculpt_value(key, value)
            self.character_system.sculpt()
            self.character_system.refresh_layers()

    def refresh_sliders(self):
        log.debug("[CharacterEditorPanel][refresh_sliders] 🔄 Synchronisiere Slider")
        for key, slider in self.sliders.items():
            new_val = self.character_system.sculpt_data.get(key, 50)
            if slider.value() != new_val:
                slider.setValue(new_val)

    def set_male(self):
        log.info("[CharacterEditorPanel] ♂ Männlich gewählt")
        try:
            self.character_system.set_gender("male")
            self.character_system.load_base_model("male")
            self.character_system.refresh_viewport()
        except Exception as e:
            log.error(f"[CharacterEditorPanel][set_male] ❌ Fehler: {e}")

    def set_female(self):
        log.info("[CharacterEditorPanel] ♀ Weiblich gewählt")
        try:
            self.character_system.set_gender("female")
            self.character_system.load_base_model("female")
            self.character_system.refresh_viewport()
        except Exception as e:
            log.error(f"[CharacterEditorPanel][set_female] ❌ Fehler: {e}")
