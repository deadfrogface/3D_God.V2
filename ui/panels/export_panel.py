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
