from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QTabWidget, QMenuBar, QMenu, QStatusBar,
    QDockWidget, QToolBar, QAction
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QKeySequence
from pathlib import Path

# Import all panels
from ui.panels.ai_generator_panel import AIGeneratorPanel
from ui.panels.character_editor import CharacterEditorPanel
from ui.panels.sculpt_panel import SculptPanel
from ui.panels.anatomy_viewer import AnatomyViewer
from ui.panels.clothing_panel import ClothingPanel
from ui.panels.rigging_panel import RiggingPanel
from ui.panels.nsfw_panel import NSFWPanel
from ui.panels.export_panel import ExportPanel
from ui.viewport_3d import Viewport3D

class MainWindow(QMainWindow):
    def __init__(self, config, character_system, ai_generator):
        super().__init__()
        self.config = config
        self.character_system = character_system
        self.ai_generator = ai_generator

        self.setWindowTitle("🔱 3D_God - Character Creator")
        self.setMinimumSize(1600, 900)

        self.load_theme()
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_central_widget()
        self.create_dock_widgets()
        self.create_status_bar()
        self.load_window_state()

    def load_theme(self):
        theme_name = self.config.get("theme", "cyberpunk")
        theme_path = f"ui/themes/{theme_name}.qss"
        try:
            with open(theme_path, 'r') as f:
                self.setStyleSheet(f.read())
        except:
            self.setStyleSheet("""
                QMainWindow { background-color: #0a0a0a; color: #00ff88; }
                QTabWidget::pane { border: 2px solid #00ff88; background-color: #1a1a1a; }
                QTabBar::tab {
                    background-color: #2a2a2a;
                    color: #00ff88;
                    padding: 8px 16px;
                    margin: 2px;
                    border: 1px solid #444;
                    font-weight: bold;
                }
                QTabBar::tab:selected {
                    background-color: #00ff88;
                    color: #000000;
                    border: 2px solid #00ffff;
                }
                QPushButton {
                    background-color: #2a2a2a;
                    color: #00ff88;
                    border: 2px solid #00ff88;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #00ff88;
                    color: #000000;
                }
                QDockWidget { color: #00ff88; font-weight: bold; }
                QDockWidget::title {
                    background-color: #1a1a1a;
                    border: 1px solid #00ff88;
                    padding: 4px;
                }
            """)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Datei-Menü
        file_menu = menubar.addMenu("📁 Datei")

        new_action = QAction("🆕 Neuer Charakter", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_character)
        file_menu.addAction(new_action)

        load_action = QAction("📂 Charakter laden", self)
        load_action.setShortcut(QKeySequence.Open)
        file_menu.addAction(load_action)

        save_action = QAction("💾 Charakter speichern", self)
        save_action.setShortcut(QKeySequence.Save)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        # Preset-Menü
        preset_menu = file_menu.addMenu("👥 Presets laden")
        preset_folder = Path("assets/character_presets")
        preset_folder.mkdir(parents=True, exist_ok=True)
        presets = [f.stem for f in preset_folder.glob("*.json")]

        for preset in presets:
            action = QAction(f"🎭 {preset}", self)
            action.triggered.connect(lambda checked, p=preset: self.load_preset(p))
            preset_menu.addAction(action)

        file_menu.addSeparator()
        exit_action = QAction("❌ Beenden", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Bearbeiten-Menü
        edit_menu = menubar.addMenu("✏️ Bearbeiten")
        edit_menu.addAction(QAction("↩️ Rückgängig", self))
        edit_menu.addAction(QAction("↪️ Wiederholen", self))

        # Ansicht-Menü
        view_menu = menubar.addMenu("👁️ Ansicht")

        nsfw_action = QAction("🔞 NSFW-Modus", self)
        nsfw_action.setCheckable(True)
        nsfw_action.setChecked(self.config.get("nsfw_enabled", True))
        nsfw_action.triggered.connect(self.toggle_nsfw)
        view_menu.addAction(nsfw_action)

        anatomy_menu = view_menu.addMenu("🦴 Anatomie-Layer")
        for layer in ["Haut", "Fett", "Muskeln", "Knochen", "Organe"]:
            action = QAction(f"👁️ {layer}", self)
            action.setCheckable(True)
            action.setChecked(True)
            anatomy_menu.addAction(action)

        tools_menu = menubar.addMenu("🔧 Werkzeuge")
        tools_menu.addAction(QAction("🎨 Sculpting-Modus", self))
        tools_menu.addAction(QAction("🦴 Auto-Rigging", self))

        help_menu = menubar.addMenu("❓ Hilfe")
        help_menu.addAction(QAction("🎮 Controller-Mapping", self))
        help_menu.addAction(QAction("ℹ️ Über 3D_God", self))

    def create_tool_bar(self):
        toolbar = QToolBar("Hauptwerkzeuge")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)

        toolbar.addAction(QAction("🆕", self))
        toolbar.addAction(QAction("💾", self))
        toolbar.addSeparator()
        toolbar.addAction(QAction("🤖", self, triggered=lambda: self.tab_widget.setCurrentIndex(0)))
        toolbar.addAction(QAction("🧍", self, triggered=lambda: self.tab_widget.setCurrentIndex(1)))
        toolbar.addAction(QAction("🎨", self, triggered=lambda: self.tab_widget.setCurrentIndex(2)))
        toolbar.addAction(QAction("👕", self, triggered=lambda: self.tab_widget.setCurrentIndex(3)))
        toolbar.addAction(QAction("🦴", self, triggered=lambda: self.tab_widget.setCurrentIndex(4)))
        toolbar.addAction(QAction("📤", self, triggered=lambda: self.tab_widget.setCurrentIndex(5)))

    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.West)

        self.ai_panel = AIGeneratorPanel(self.ai_generator)
        self.tab_widget.addTab(self.ai_panel, "🤖 KI-Generator")

        self.character_panel = CharacterEditorPanel(self.character_system)
        self.tab_widget.addTab(self.character_panel, "🧍 Character")

        self.sculpt_panel = SculptPanel(self.character_system)
        self.tab_widget.addTab(self.sculpt_panel, "🎨 Sculpting")

        self.clothing_panel = ClothingPanel(self.character_system)
        self.tab_widget.addTab(self.clothing_panel, "👕 Kleidung")

        self.rigging_panel = RiggingPanel(self.character_system)
        self.tab_widget.addTab(self.rigging_panel, "🦴 Rigging")

        self.export_panel = ExportPanel(self.character_system)
        self.tab_widget.addTab(self.export_panel, "📤 Export")

        splitter.addWidget(self.tab_widget)

        self.viewport = Viewport3D(self.character_system)
        splitter.addWidget(self.viewport)

        splitter.setSizes([640, 960])

    def create_dock_widgets(self):
        anatomy_dock = QDockWidget("🦴 Anatomie-Viewer", self)
        self.anatomy_viewer = AnatomyViewer(self.character_system)
        anatomy_dock.setWidget(self.anatomy_viewer)
        self.addDockWidget(Qt.RightDockWidgetArea, anatomy_dock)

        if self.config.get("nsfw_enabled", True):
            nsfw_dock = QDockWidget("🔞 NSFW-Kontrollen", self)
            self.nsfw_panel = NSFWPanel(self.character_system)
            nsfw_dock.setWidget(self.nsfw_panel)
            self.addDockWidget(Qt.RightDockWidgetArea, nsfw_dock)
            self.tabifyDockWidget(anatomy_dock, nsfw_dock)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🔱 3D_God bereit | 🎮 Controller: Nicht verbunden")

    def new_character(self):
        self.character_system.new_character()
        self.viewport.update_view()
        self.status_bar.showMessage("✨ Neuer Charakter erstellt")

    def load_preset(self, preset_name):
        if self.character_system.load_preset(preset_name):
            self.viewport.update_view()
            self.status_bar.showMessage(f"✅ Preset geladen: {preset_name}")
        else:
            self.status_bar.showMessage(f"❌ Fehler beim Laden: {preset_name}")

    def toggle_nsfw(self, checked):
        self.config["nsfw_enabled"] = checked
        self.character_system.set_nsfw_mode(checked)
        self.viewport.update_view()

        for dock in self.findChildren(QDockWidget):
            if "NSFW" in dock.windowTitle():
                dock.setVisible(checked)

        self.status_bar.showMessage(
            f"🔞 NSFW-Modus: {'Aktiviert' if checked else 'Deaktiviert'}"
        )

    def load_window_state(self):
        pass

    def closeEvent(self, event):
        event.accept()