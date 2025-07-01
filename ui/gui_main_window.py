from PySide6.QtWidgets import QMainWindow, QTabWidget, QSplitter, QStatusBar
from PySide6.QtCore import Qt

from ui.panels.settings_panel import SettingsPanel
from ui.panels.character_editor import CharacterEditor
from ui.panels.sculpt_panel import SculptPanel
from ui.panels.anatomy_viewer import AnatomyViewer
from ui.panels.rigging_panel import RiggingPanel
from ui.panels.export_panel import ExportPanel
from ui.panels.ai_prompt_panel import AIPromptPanel
from ui.panels.clothing_panel import ClothingPanel
from ui.panels.debug_console import DebugConsole
from ui.viewport.viewport_3d import Viewport3D
from ui.panels.preset_browser import PresetBrowser
from ui.style_manager import StyleManager

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        StyleManager.apply_theme(config.get("theme", "dark"))
        self.setWindowTitle("3D God Creator")
        self.setGeometry(100, 100, 1600, 900)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def launch_main_gui(self):
        self.tab_widget = QTabWidget()

self.tab_widget.addTab(PresetBrowser(), "Presets")
        self.tab_widget.addTab(CharacterEditor(), "Körper")
        self.tab_widget.addTab(SculptPanel(), "Sculpting")
        self.tab_widget.addTab(AnatomyViewer(), "Anatomie")
        self.tab_widget.addTab(RiggingPanel(), "Rigging")
        self.tab_widget.addTab(ClothingPanel(), "Kleidung")
        self.tab_widget.addTab(ExportPanel(), "Export")
        self.tab_widget.addTab(AIPromptPanel(), "KI")
        self.tab_widget.addTab(SettingsPanel(), "Einstellungen")

        self.viewport = Viewport3D()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tab_widget)
        splitter.addWidget(self.viewport)
        self.setCentralWidget(splitter)

        self.debug_console = DebugConsole()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.debug_console)
        self.status.showMessage("3D God bereit")