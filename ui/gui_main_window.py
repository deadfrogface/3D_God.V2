from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QTabWidget, QDockWidget, QStatusBar, QTextEdit
)
from PySide6.QtCore import Qt

# Panels
from ui.panels.ai_generator_panel import AIGeneratorPanel
from ui.panels.character_editor import CharacterEditorPanel
from ui.panels.sculpt_panel import SculptPanel
from ui.panels.anatomy_viewer import AnatomyViewer
from ui.panels.clothing_panel import ClothingPanel
from ui.panels.rigging_panel import RiggingPanel
from ui.panels.export_panel import ExportPanel
from ui.panels.nsfw_panel import NSFWPanel
from ui.viewport_3d import Viewport3D


class MainWindow(QMainWindow):
    def __init__(self, config, character_system, ai_generator):
        super().__init__()
        self.config = config
        self.character_system = character_system
        self.ai_generator = ai_generator

        self.setWindowTitle("🔱 3D_God - Character Creator")
        self.setMinimumSize(1600, 900)

        self.setup_ui()

    def setup_ui(self):
        """Set up main GUI layout"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.West)
        self.tab_widget.addTab(AIGeneratorPanel(self.ai_generator), "🤖 KI")
        self.tab_widget.addTab(CharacterEditorPanel(self.character_system), "🧍 Körperform")
        self.tab_widget.addTab(SculptPanel(self.character_system), "🎨 Sculpting")
        self.tab_widget.addTab(ClothingPanel(self.character_system), "👕 Kleidung")
        self.tab_widget.addTab(RiggingPanel(self.character_system), "🦴 Rigging")
        self.tab_widget.addTab(ExportPanel(self.character_system), "📤 Export")
        splitter.addWidget(self.tab_widget)

        # Viewport
        self.viewport = Viewport3D(self.character_system)
        splitter.addWidget(self.viewport)
        splitter.setStretchFactor(1, 1)

        # Docks
        self.setup_docks()

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("🔱 3D_God bereit")

    def setup_docks(self):
        """Add dock panels (anatomy, NSFW, log)"""
        self.anatomy_dock = QDockWidget("🦴 Anatomie", self)
        self.anatomy_dock.setWidget(AnatomyViewer(self.character_system))
        self.addDockWidget(Qt.RightDockWidgetArea, self.anatomy_dock)

        if self.config.get("nsfw_enabled", True):
            self.nsfw_dock = QDockWidget("🔞 NSFW", self)
            self.nsfw_dock.setWidget(NSFWPanel(self.character_system))
            self.addDockWidget(Qt.RightDockWidgetArea, self.nsfw_dock)
            self.tabifyDockWidget(self.anatomy_dock, self.nsfw_dock)

        self.log_dock = QDockWidget("📜 Log-Konsole", self)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_dock.setWidget(self.log_output)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

    def log(self, text):
        """Append text to log console"""
        self.log_output.append(text)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

    def update_view(self):
        self.viewport.update_view()