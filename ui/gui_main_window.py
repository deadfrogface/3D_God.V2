from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QSplitter, QStatusBar, QShortcut
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

from ui.panels.settings_panel import SettingsPanel
from ui.panels.character_editor_panel import CharacterEditorPanel
from ui.panels.sculpt_panel import SculptPanel
from ui.panels.nsfw_panel import NSFWPanel
from ui.panels.export_panel import ExportPanel
from ui.panels.rigging_panel import RiggingPanel
from ui.panels.clothing_panel import ClothingPanel
from ui.panels.ai_panel import AIPanel
from ui.viewport.viewport_3d import Viewport3D
from ui.style_manager import StyleManager
from ui.debug_console import DebugConsole
from core.character_system.character_system import CharacterSystem

import os

class MainWindow(QMainWindow):
    def __init__(self, config):
        print("[MainWindow][__init__] ▶️ Initialisiere mit Konfiguration:", config)
        super().__init__()
        self.config = config
        StyleManager.apply_theme(config.get("theme", "dark"))

        self.setWindowTitle("3D God Creator")
        self.setGeometry(100, 100, 1600, 900)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.tabs = QTabWidget()
        self.viewport = Viewport3D()
        self.debug_console = DebugConsole()
        self.debug_console.hide()

        self.splitter = QSplitter()
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.viewport)
        self.setCentralWidget(self.splitter)

        self.shortcut_debug = QShortcut(QKeySequence("F12"), self)
        self.shortcut_debug.activated.connect(self.toggle_debug_console)

        self.character_system = CharacterSystem()
        self.character_system.bind_viewport(self.viewport)

        if os.path.exists("presets/default.json"):
            print("[MainWindow] Lade Standard-Preset...")
            self.character_system.load_preset("default")

        self.launch_main_gui()

    def toggle_debug_console(self):
        print("[MainWindow][toggle_debug_console] ▶️ Umschalten")
        if self.debug_console.isVisible():
            self.debug_console.hide()
            print("[MainWindow] 🔽 Debug-Konsole versteckt")
        else:
            self.debug_console.show()
            print("[MainWindow] 🔼 Debug-Konsole angezeigt")

    def launch_main_gui(self):
        print("[MainWindow][launch_main_gui] ▶️ Tabs werden geladen...")
        self.tabs.addTab(CharacterEditorPanel(self.character_system), "🧍 Form")
        self.tabs.addTab(SculptPanel(self.character_system), "🪨 Sculpt")
        self.tabs.addTab(NSFWPanel(self.character_system), "🔞 NSFW")
        self.tabs.addTab(ClothingPanel(self.character_system), "👕 Kleidung")
        self.tabs.addTab(RiggingPanel(self.character_system), "🦴 Rigging")
        self.tabs.addTab(ExportPanel(), "📤 Export")
        self.tabs.addTab(SettingsPanel(), "⚙️ Einstellungen")
        self.tabs.addTab(AIPanel(self.character_system), "🧠 KI")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.debug_console)
        print("[MainWindow] ✅ GUI geladen")