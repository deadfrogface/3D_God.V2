from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QHBoxLayout
)
from core.character_system.character_system import CharacterSystem
from core.logger import log
import os
import shutil


class ExportPanel(QWidget):
    def __init__(self, character_system: CharacterSystem):
        try:
            super().__init__()
            self.character_system = character_system
            log.info("[ExportPanel][__init__] ▶️ Initialisierung gestartet")

            layout = QVBoxLayout()
            layout.addWidget(QLabel("📦 Modell-Export"))

            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("Dateiname:"))
            self.name_input = QLineEdit("my_character")
            name_layout.addWidget(self.name_input)
            layout.addLayout(name_layout)

            btn_save = QPushButton("💾 Preset speichern")
            btn_save.clicked.connect(self.save_preset)
            layout.addWidget(btn_save)

            btn_export = QPushButton("📤 FBX exportieren")
            btn_export.clicked.connect(self.export_fbx)
            layout.addWidget(btn_export)

            layout.addWidget(QLabel("📂 Unreal-Zielordner"))
            self.unreal_path = QLineEdit("")
            self.unreal_path.setPlaceholderText("z. B. C:/Projekte/UE5/YourGame/Content/Characters")
            layout.addWidget(self.unreal_path)

            btn_browse = QPushButton("📁 Ordner wählen")
            btn_browse.clicked.connect(self.choose_unreal_folder)
            layout.addWidget(btn_browse)

            btn_unreal = QPushButton("🚀 Exportiere nach Unreal")
            btn_unreal.clicked.connect(self.export_to_unreal)
            layout.addWidget(btn_unreal)

            layout.addWidget(QLabel("📝 Export-Log"))
            self.logbox = QTextEdit()
            self.logbox.setReadOnly(True)
            self.logbox.setPlaceholderText("Exportmeldungen erscheinen hier...")
            layout.addWidget(self.logbox)

            self.setLayout(layout)
            log.info("[ExportPanel][__init__] ✅ Initialisierung abgeschlossen")
        except Exception as e:
            log.error(f"[ExportPanel][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def write_log(self, message: str, level="INFO"):
        if level == "INFO":
            log.info(message)
        elif level == "ERROR":
            log.error(message)
        elif level == "SUCCESS" and hasattr(log, "success"):
            log.success(message)
        else:
            log.info(message)
        self.logbox.append(message)

    def save_preset(self):
        name = self.name_input.text()
        self.write_log(f"[ExportPanel][save_preset] ▶️ Speichere Preset: {name}")
        self.character_system.save_preset(name)
        self.write_log(f"[ExportPanel][save_preset] ✅ Preset gespeichert: {name}", "SUCCESS")

    def export_fbx(self):
        name = self.name_input.text()
        self.write_log("[ExportPanel][export_fbx] ▶️ Starte FBX-Export")
        try:
            self.character_system.save_preset(name)
            self.character_system.export_model()
            self.write_log(f"[ExportPanel][export_fbx] ✅ FBX-Export abgeschlossen: exports/{name}.fbx", "SUCCESS")
            if self.character_system.viewport_ref:
                self.character_system.viewport_ref.load_preview("exports/preview.glb")
                self.write_log("[ExportPanel][export_fbx] ✅ Vorschau aktualisiert", "SUCCESS")
        except Exception as e:
            self.write_log(f"[ExportPanel][export_fbx] ❌ Fehler beim Export: {e}", "ERROR")

    def choose_unreal_folder(self):
        self.write_log("[ExportPanel][choose_unreal_folder] ▶️ Benutzer wählt Unreal-Zielverzeichnis")
        path = QFileDialog.getExistingDirectory(self, "Unreal-Zielordner wählen")
        if path:
            self.unreal_path.setText(path)
            self.write_log(f"[ExportPanel][choose_unreal_folder] ✅ Unreal-Zielordner gesetzt: {path}", "SUCCESS")
        else:
            self.write_log("[ExportPanel][choose_unreal_folder] ❌ Keine Auswahl getroffen", "ERROR")

    def export_to_unreal(self):
        name = self.name_input.text()
        src_fbx = os.path.join("exports", f"{name}.fbx")
        dst_dir = self.unreal_path.text().strip()
        self.write_log(f"[ExportPanel][export_to_unreal] ▶️ Starte Kopiervorgang nach: {dst_dir}")

        if not dst_dir or not os.path.exists(dst_dir):
            self.write_log("[ExportPanel][export_to_unreal] ❌ Fehler: Ungültiger Unreal-Zielpfad.", "ERROR")
            return

        try:
            dst_fbx = os.path.join(dst_dir, f"{name}.fbx")
            shutil.copy(src_fbx, dst_fbx)
            self.write_log(f"[ExportPanel][export_to_unreal] ✅ FBX kopiert nach Unreal: {dst_fbx}", "SUCCESS")
        except Exception as e:
            self.write_log(f"[ExportPanel][export_to_unreal] ❌ Fehler beim Kopieren: {e}", "ERROR")
