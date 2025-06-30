from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QMenuBar, QMenu, QAction, QStatusBar)
import sys

class MainWindow(QMainWindow):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.setWindowTitle("3D_God")
        self.setMinimumSize(1200, 800)

        self.create_menu()
        self.create_status_bar()
        self.create_tabs()

    def create_menu(self):
        menubar = self.menuBar()

        view_menu = menubar.addMenu("👁️ Ansicht")

        # 🔞 NSFW-Modus Toggle
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
        self.create_tab("Export")

    def create_tab(self, name):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)

    def toggle_nsfw(self, checked):
        self.character_system.set_nsfw_mode(checked)
        status = "An" if checked else "Aus"
        self.status_bar.showMessage(f"🔞 NSFW-Modus: {status}")

if __name__ == "__main__":
    from core.character_system.character_system import CharacterSystem  # Dummy-Klasse

    app = QApplication(sys.argv)
    character_system = CharacterSystem()
    window = MainWindow(character_system)
    window.show()
    sys.exit(app.exec())
