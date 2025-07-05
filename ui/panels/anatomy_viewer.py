from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from core.character_system.character_system import CharacterSystem
from core.logger import log

class AnatomyViewer(QWidget):
    def __init__(self, character_system: CharacterSystem):
        try:
            super().__init__()
            self.character_system = character_system
            self.character_system.anatomy_sync_callback = self.sync_checkboxes

            log.info("[AnatomyViewer][__init__] ▶️ Initialisiere Anatomie-Viewer")

            layout = QVBoxLayout()
            layout.addWidget(QLabel("🧬 Anatomie-Viewer"))

            self.checkboxes = {}

            for layer in ["skin", "fat", "muscle", "bone", "organs"]:
                checkbox = QCheckBox(layer.capitalize())
                checkbox.setChecked(self.character_system.anatomy_state.get(layer, False))
                checkbox.stateChanged.connect(lambda state, l=layer: self.toggle_layer(l, state))
                layout.addWidget(checkbox)
                self.checkboxes[layer] = checkbox

            self.setLayout(layout)
            log.info("[AnatomyViewer][__init__] ✅ Panel bereit")
        except Exception as e:
            log.error(f"[AnatomyViewer][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def toggle_layer(self, layer, state):
        value = state == 2
        self.character_system.update_anatomy_layer(layer, value)
        log.info(f"[AnatomyViewer][toggle_layer] 🧩 Layer '{layer}' gesetzt auf: {value}")

    def sync_checkboxes(self):
        for layer, checkbox in self.checkboxes.items():
            new_state = self.character_system.anatomy_state.get(layer, False)
            checkbox.setChecked(new_state)
        log.debug("[AnatomyViewer][sync_checkboxes] 🔁 Checkbox-Zustände synchronisiert")
