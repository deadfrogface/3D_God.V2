from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
from PySide6.QtCore import Qt

class SculptPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🎨 Sculpting-System")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Sculpting starten
        sculpt_btn = QPushButton("🧱 Sculpting starten")
        sculpt_btn.clicked.connect(self.start_sculpting)
        layout.addWidget(sculpt_btn)

        # Symmetrie auswählen
        sym_layout = QHBoxLayout()
        sym_label = QLabel("🌀 Achsensymmetrie:")
        self.sym_box = QComboBox()
        self.sym_box.addItems(["X", "Y", "Z"])
        sym_btn = QPushButton("🔁 Anwenden")
        sym_btn.clicked.connect(self.apply_symmetry)

        sym_layout.addWidget(sym_label)
        sym_layout.addWidget(self.sym_box)
        sym_layout.addWidget(sym_btn)
        layout.addLayout(sym_layout)

        # Blender Skript
        blender_btn = QPushButton("🧠 Blender-Skript ausführen")
        blender_btn.clicked.connect(lambda: self.character_system.run_blender_script("test_script.py"))
        layout.addWidget(blender_btn)

        # Statusanzeige
        self.status = QLabel("⏳ Bereit")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def start_sculpting(self):
        self.status.setText("🎨 Starte Sculpting...")
        self.character_system.sculpt()
        self.status.setText("✅ Sculpting ausgeführt")

    def apply_symmetry(self):
        axis = self.sym_box.currentText()
        if self.character_system.sculpt_tools:
            self.character_system.sculpt_tools.apply_symmetry(axis)
            self.status.setText(f"✅ Symmetrie angewendet: {axis}")
        else:
            self.status.setText("❌ Sculpting-Werkzeug nicht verfügbar")