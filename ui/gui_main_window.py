from PySide6.QtWidgets import QMainWindow, QTabWidget, QSplitter, QStatusBar
from PySide6.QtCore import Qt
from ui.panels.character_editor import CharacterEditor
from ui.panels.sculpt_panel import SculptPanel
from ui.panels.anatomy_viewer import AnatomyViewer
from ui.panels.rigging_panel import RiggingPanel
from ui.panels.export_panel import ExportPanel
from ui.panels.ai_prompt_panel import AIPromptPanel
from ui.panels.settings_panel import SettingsPanel
from ui.panels.debug_console import DebugConsole
from ui.panels.preset_browser import PresetBrowser
from ui.panels.clothing_panel import ClothingPanel
from ui.panels.material_editor import MaterialEditor
from ui.panels.physics_panel import PhysicsPanel
from ui.panels.rig_viewer import RigViewer
from ui.viewport.viewport_3d import Viewport3D
from core.controller.controller_input import ControllerInput
from ui.style_manager import StyleManager
from core.character_system.character_system import CharacterSystem

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        StyleManager.apply_theme(config.get("theme", "dark"))
        self.setWindowTitle("3D God Creator")
        self.setGeometry(100, 100, 1600, 900)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.controller_enabled = config.get("controller_enabled", True)
        self.controller = None

    def launch_main_gui(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(CharacterEditor(), "Körper")
        self.tab_widget.addTab(SculptPanel(), "Sculpting")
        self.tab_widget.addTab(AnatomyViewer(), "Anatomie")
        self.tab_widget.addTab(RiggingPanel(), "Rigging")
        self.tab_widget.addTab(ExportPanel(), "Export")
        self.tab_widget.addTab(AIPromptPanel(), "KI")
        self.tab_widget.addTab(ClothingPanel(), "Assets")
        self.tab_widget.addTab(MaterialEditor(), "Material")
        self.tab_widget.addTab(PhysicsPanel(), "Physik")
        self.tab_widget.addTab(RigViewer(), "Rig-Viewer")
        self.tab_widget.addTab(PresetBrowser(), "Presets")
        self.tab_widget.addTab(SettingsPanel(), "Einstellungen")

        self.debug_console = DebugConsole()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.debug_console)

        self.viewport = Viewport3D()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tab_widget)
        splitter.addWidget(self.viewport)
        self.setCentralWidget(splitter)

        cs = CharacterSystem()
        cs.bind_viewport(self.viewport)

        self.status.showMessage("3D God bereit")

        if self.controller_enabled:
            self.controller = ControllerInput(self.switch_tab)
            self.controller.start()

    def switch_tab(self, direction):
        current = self.tab_widget.currentIndex()
        count = self.tab_widget.count()
        new_index = (current + direction) % count
        self.tab_widget.setCurrentIndex(new_index)