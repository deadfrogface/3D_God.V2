from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QMenuBar, QMenu, QAction, QStatusBar, QDockWidget
)
from PySide6.QtCore import Qt
from ui.panels.nsfw_panel import NSFWPanel
from ui.panels.export_panel import ExportPanel

class MainWindow(QMainWindow):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.setWindowTitle("🔱 3D_God")
        self.setMinimumSize(1200, 800)

        self.create_menu()
        self.create_status_bar()
        self.create_tabs()
        self.create_nsfw_dock()

    def create_menu(self):
        menubar = self.menuBar()

        # 📁 Datei-Menü
        file_menu = menubar.addMenu("📁 Datei")

        # 👥 Presets laden
        load_preset_menu = file_menu.addMenu("👥 Presets laden")
        for name in ["Brakka", "Dogmeat", "Bogg"]:
            action = QAction(f"{name}", self)
            action.triggered.connect(lambda checked, n=name: self.load_preset(n))
            load_preset_menu.addAction(action)

        # 👁️ Ansicht-Menü
        view_menu = menubar.addMenu("👁️ Ansicht")

        # 🔞 NSFW-Toggle
        self.nsfw_action = QAction("🔞 NSFW-Modus", self)
        self.nsfw_action.setCheckable(True)
        self.nsfw_action.setChecked(True)
        self.nsfw_action.triggered.connect(self.toggle_nsfw)
        view_menu.addAction(self.nsfw_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🔱 3D_God gestartet – NSFW-Modus: An")

    def create_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tab("Charakter")
        self.create_tab("Kleidung")
        self.create_tab("KI")
        self.create_tab("Rigging")

        # NEU: Export-Tab mit Panel
        export_tab = ExportPanel(self.character_system)
        self.tabs.addTab(export_tab, "📤 Export")

    def create_tab(self, name):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)

    def create_nsfw_dock(self):
        nsfw_dock = QDockWidget("🔞 NSFW-Kontrollen", self)
        self.nsfw_panel = NSFWPanel(self.character_system)
        nsfw_dock.setWidget(self.nsfw_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, nsfw_dock)

    def toggle_nsfw(self, checked):
        self.character_system.set_nsfw_mode(checked)
        status = "An" if checked else "Aus"
        self.status_bar.showMessage(f"🔞 NSFW-Modus: {status}")

    def load_preset(self, name):
        if self.character_system.load_preset(name):
            self.status_bar.showMessage(f"✅ Preset geladen: {name}")
        else:
            self.status_bar.showMessage(f"❌ Fehler beim Laden: {name}")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from core.character_system.character_system import CharacterSystem

    app = QApplication(sys.argv)
    character_system = CharacterSystem()
    window = MainWindow(character_system)
    window.show()
    sys.exit(app.exec())
