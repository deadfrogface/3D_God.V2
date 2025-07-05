from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QSplitter, QStatusBar,
    QDockWidget, QShortcut
)
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Qt

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
from ui.panels.debug_console import DebugConsole
from core.character_system.character_system import CharacterSystem
from core.logger import log

import os

class MainWindow(QMainWindow):
    def __init__(self, config):
        log.info("[MainWindow][__init__] Initialisiere mit Konfiguration...")
        super().__init__()
        self.config = config

        # 🧠 CharacterSystem vorbereiten
        self.character_system = CharacterSystem()
        StyleManager.apply_theme(config.get("theme", "dark"))

        # 🪟 Fenster-Setup
        self.setWindowTitle("3D God Creator")
        self.setGeometry(100, 100, 1600, 900)
        self.setStatusBar(QStatusBar())

        # 🧭 Tabs & Viewport
        self.tabs = QTabWidget()
        self.viewport = Viewport3D(self.character_system)

        # 🐞 Debug-Konsole als DockWidget
        self.debug_console = DebugConsole()
        self.dock_debug = QDockWidget("🛠 Debug-Konsole", self)
        self.dock_debug.setWidget(self.debug_console)
        self.dock_debug.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.dock_debug.setFloating(False)
        self.dock_debug.hide()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_debug)

        # ➗ Hauptlayout
        self.splitter = QSplitter()
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.viewport)
        self.setCentralWidget(self.splitter)

        # 🔁 Shortcuts
        self.shortcut_debug = QShortcut(QKeySequence("F12"), self)
        self.shortcut_debug.activated.connect(self.toggle_debug_console)

        # 🔗 Viewport verbinden
        self.character_system.bind_viewport(self.viewport)

        # 🎯 Preset laden
        if os.path.exists("presets/default.json"):
            log.info("[MainWindow] Lade Standard-Preset...")
            self.character_system.load_preset("default")

        # 🚀 GUI aufbauen
        self.launch_main_gui()

    def toggle_debug_console(self):
        log.info("[MainWindow][toggle_debug_console] Umschalten...")
        if self.dock_debug.isVisible():
            self.dock_debug.hide()
            log.info("[MainWindow] 🔽 Debug-Konsole versteckt")
        else:
            self.dock_debug.show()
            log.info("[MainWindow] 🔼 Debug-Konsole angezeigt")

    def launch_main_gui(self):
        log.info("[MainWindow][launch_main_gui] Tabs werden geladen...")
        self.tabs.addTab(CharacterEditorPanel(self.character_system), "🧍 Form")
        self.tabs.addTab(SculptPanel(self.character_system), "🪨 Sculpt")
        self.tabs.addTab(NSFWPanel(self.character_system), "🔞 NSFW")
        self.tabs.addTab(ClothingPanel(self.character_system), "👕 Kleidung")
        self.tabs.addTab(RiggingPanel(self.character_system), "🦴 Rigging")
        self.tabs.addTab(ExportPanel(self.character_system), "📤 Export")
        self.tabs.addTab(SettingsPanel(self.character_system), "⚙️ Einstellungen")
        self.tabs.addTab(AIPanel(self.character_system), "🧠 KI")
        log.info("[MainWindow] ✅ GUI geladen")
