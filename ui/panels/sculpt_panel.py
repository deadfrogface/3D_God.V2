from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

class SculptPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🎨 Sculpting-Modus")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Sculpting starten
        sculpt_btn = QPushButton("🧱 Sculpting starten")
        sculpt_btn.clicked.connect(self.character_system.sculpt)
        layout.addWidget(sculpt_btn)

        # Symmetrie Auswahl
        sym_layout = QHBoxLayout()
        self.axis_box = QComboBox()
        self.axis_box.addItems(["X", "Y", "Z"])
        sym_btn = QPushButton("🔁 Symmetrie anwenden")
        sym_btn.clicked.connect(self.apply_symmetry)
        sym_layout.addWidget(self.axis_box)
        sym_layout.addWidget(sym_btn)
        layout.addLayout(sym_layout)

        # Blender Script
        blender_btn = QPushButton("🧠 Blender-Skript ausführen")
        blender_btn.clicked.connect(lambda: self.character_system.run_blender_script("test_script.py"))
        layout.addWidget(blender_btn)

        self.status = QLabel("Bereit")
        layout.addWidget(self.status)

        layout.addStretch()
        self.setLayout(layout)

    def apply_symmetry(self):
        axis = self.axis_box.currentText()
        if self.character_system.sculpt_tools:
            self.character_system.sculpt_tools.apply_symmetry(axis)
            self.status.setText(f"✅ Symmetrie angewendet: {axis}")
        else:
            self.status.setText("❌ Sculpt-Tools nicht verfügbar")