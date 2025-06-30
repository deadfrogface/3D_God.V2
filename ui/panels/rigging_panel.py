from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class RiggingPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🦴 Rigging & Skeleton Setup")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        auto_btn = QPushButton("⚡ Auto-Rigging starten")
        meta_btn = QPushButton("🎭 Metahuman kompatibel machen")
        manual_btn = QPushButton("🔧 Manuelles Rigging")

        layout.addWidget(auto_btn)
        layout.addWidget(meta_btn)
        layout.addWidget(manual_btn)

        layout.addStretch()
        self.setLayout(layout)