from PySide6.QtWidgets import QMainWindow, QTabWidget, QSplitter, QStatusBar
from ui.panels.settings_panel import SettingsPanel
from ui.style_manager import StyleManager
from PySide6.QtCore import Qt

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
        from ui.panels.character_editor import CharacterEditor
        from ui.panels.sculpt_panel import SculptPanel
        from ui.panels.anatomy_viewer import AnatomyViewer
        from ui.panels.export_panel import ExportPanel
        from ui.panels.ai_prompt_panel import AIPromptPanel
        from ui.panels.rigging_panel import RiggingPanel
        from ui.panels.settings_panel import SettingsPanel

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(CharacterEditor(), "Körper")
        self.tab_widget.addTab(SculptPanel(), "Sculpting")
        self.tab_widget.addTab(AnatomyViewer(), "Anatomie")
        self.tab_widget.addTab(RiggingPanel(), "Rigging")
        self.tab_widget.addTab(ExportPanel(), "Export")
        self.tab_widget.addTab(AIPromptPanel(), "KI")
        self.tab_widget.addTab(SettingsPanel(), "Einstellungen")

        self.setCentralWidget(self.tab_widget)
        self.status.showMessage("3D God bereit")
