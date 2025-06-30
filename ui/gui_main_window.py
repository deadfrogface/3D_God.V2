from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D_God")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        for name in ["Charakter", "Kleidung", "KI", "Rigging", "Export"]:
            self.create_tab(name)

    def create_tab(self, name):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        self.tabs.addTab(tab, name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

