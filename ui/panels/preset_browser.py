from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
import os
import json
from core.character_system.character_system import CharacterSystem
from PySide6.QtGui import QPixmap, QScreen
from PySide6.QtWidgets import QApplication

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

    def refresh_list(self):
        self.preset_list.clear()
        preset_folder = "presets/"
        if not os.path.exists(preset_folder):
            os.makedirs(preset_folder)

        for file in os.listdir(preset_folder):
            if file.endswith(".json"):
                path = os.path.join(preset_folder, file)
                with open(path, "r") as f:
                    try:
                        data = json.load(f)
                        name = file.replace(".json", "")
                        nsfw = data.get("nsfw", False)
                        icon = "🔞" if nsfw else "🟢"
                        item = QListWidgetItem(f"{icon} {name}")
                        self.preset_list.addItem(item)
                    except Exception as e:
                        print(f"[PresetBrowser] Fehler beim Laden: {file} – {e}")

    def load_selected_preset(self, item):
        raw_text = item.text()
        name = raw_text.replace("🔞", "").replace("🟢", "").strip()
        self.character_system.load_preset(name)

    def save_thumbnail(self):
        selected = self.preset_list.currentItem()
        if not selected:
            print("[Screenshot] Kein Preset ausgewählt.")
            return

        raw_text = selected.text()
        name = raw_text.replace("🔞", "").replace("🟢", "").strip()
        target_path = os.path.join("presets", f"{name}.jpg")

        screen = QApplication.primaryScreen()
        if screen:
            pixmap = screen.grabWindow(self.window().winId())
            pixmap.save(target_path, "jpg")
            print(f"[Screenshot] Gespeichert als: {target_path}")