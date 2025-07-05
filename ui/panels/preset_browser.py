from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QApplication
from PySide6.QtGui import QPixmap, QScreen
import os
import json
from core.character_system.character_system import CharacterSystem
from core.logger import log

class PresetBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💾 Presets durchsuchen"))

        self.preset_list = QListWidget()
        self.preset_list.itemClicked.connect(self.load_selected_preset)
        layout.addWidget(self.preset_list)

        btn_refresh = QPushButton("🔄 Liste aktualisieren")
        btn_refresh.clicked.connect(self.refresh_list)
        layout.addWidget(btn_refresh)

        btn_screenshot = QPushButton("📸 Screenshot für ausgewähltes Preset speichern")
        btn_screenshot.clicked.connect(self.save_thumbnail)
        layout.addWidget(btn_screenshot)

        self.setLayout(layout)
        self.refresh_list()
        log.info("[PresetBrowser][__init__] ✅ Preset-Browser initialisiert.")

    def refresh_list(self):
        self.preset_list.clear()
        preset_folder = "presets/"
        log.info("[PresetBrowser][refresh_list] ▶️ Lese Presets aus Ordner...")

        if not os.path.exists(preset_folder):
            os.makedirs(preset_folder)
            log.info(f"[PresetBrowser][refresh_list] 📂 Ordner erstellt: {preset_folder}")

        for file in os.listdir(preset_folder):
            if file.endswith(".json"):
                path = os.path.join(preset_folder, file)
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                        name = file.replace(".json", "")
                        nsfw = data.get("nsfw", False)
                        icon = "🔞" if nsfw else "🟢"
                        item = QListWidgetItem(f"{icon} {name}")
                        self.preset_list.addItem(item)
                        log.info(f"[PresetBrowser][refresh_list] ✅ Hinzugefügt: {name}")
                except Exception as e:
                    log.error(f"[PresetBrowser][refresh_list] ❌ Fehler beim Laden von {file}: {e}")

    def load_selected_preset(self, item):
        raw_text = item.text()
        name = raw_text.replace("🔞", "").replace("🟢", "").strip()
        log.info(f"[PresetBrowser][load_selected_preset] ▶️ Lade Preset: {name}")
        self.character_system.load_preset(name)

    def save_thumbnail(self):
        selected = self.preset_list.currentItem()
        if not selected:
            log.error("[PresetBrowser][save_thumbnail] ❌ Kein Preset ausgewählt.")
            return

        raw_text = selected.text()
        name = raw_text.replace("🔞", "").replace("🟢", "").strip()
        target_path = os.path.join("presets", f"{name}.jpg")

        screen = QApplication.primaryScreen()
        if screen:
            pixmap = screen.grabWindow(self.window().winId())
            pixmap.save(target_path, "jpg")
            log.info(f"[PresetBrowser][save_thumbnail] ✅ Screenshot gespeichert als: {target_path}")
        else:
            log.error("[PresetBrowser][save_thumbnail] ❌ Kein Bildschirm verfügbar für Screenshot.")
