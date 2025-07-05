from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QColorDialog
from core.logger import log

class MaterialEditor(QWidget):
    def __init__(self, character_system):
        try:
            super().__init__()
            self.character_system = character_system
            log.info("[MaterialEditor][__init__] ▶️ Initialisierung gestartet")

            layout = QVBoxLayout()
            layout.addWidget(QLabel("🎨 Materialeditor"))

            self.mat_select = QComboBox()
            self.mat_select.addItems(["skin", "clothes", "piercings", "tattoos"])
            layout.addWidget(self.mat_select)

            btn_color = QPushButton("Farbe wählen")
            btn_color.clicked.connect(self.choose_color)
            layout.addWidget(btn_color)

            btn_apply = QPushButton("Auf Preview anwenden")
            btn_apply.clicked.connect(self.apply_preview_material)
            layout.addWidget(btn_apply)

            self.setLayout(layout)
            log.info("[MaterialEditor][__init__] ✅ Initialisierung abgeschlossen")
        except Exception as e:
            log.error(f"[MaterialEditor][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def choose_color(self):
        current_mat = self.mat_select.currentText()
        old_hex = self.character_system.materials.get(current_mat, {}).get("color", "#cccccc")
        log.info(f"[MaterialEditor][choose_color] ▶️ Aktuelles Material: {current_mat}, alte Farbe: {old_hex}")
        color = QColorDialog.getColor()
        if color.isValid():
            hex_value = color.name()
            self.character_system.set_material_color(current_mat, hex_value)
            log.info(f"[MaterialEditor][choose_color] ✅ Neue Farbe gesetzt für {current_mat}: {hex_value}")
        else:
            log.error("[MaterialEditor][choose_color] ❌ Ungültige Farbauswahl")

    def apply_preview_material(self):
        log.info("[MaterialEditor][apply_preview_material] ▶️ Anwenden auf Vorschau gestartet")
        if self.character_system.viewport_ref:
            self.character_system.viewport_ref.show_materials(self.character_system.materials)
            log.info("[MaterialEditor][apply_preview_material] ✅ Vorschau aktualisiert")
        else:
            log.error("[MaterialEditor][apply_preview_material] ❌ Kein Viewport verbunden")
