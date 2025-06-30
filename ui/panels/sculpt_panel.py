from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout

class SculptPanel(QWidget):
    def __init__(self, character_system):
        super().__init__()
        self.character_system = character_system
        layout = QVBoxLayout()

        self.label = QLabel("🎨 Sculpting")
        layout.addWidget(self.label)

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

        self.status = QLabel("")
        layout.addWidget(self.status)
        self.setLayout(layout)

    def apply_symmetry(self):
        axis = self.axis_box.currentText()
        self.character_system.sculpt_tools.apply_symmetry(axis)
        self.status.setText(f"✅ Symmetrie angewendet: {axis}")
