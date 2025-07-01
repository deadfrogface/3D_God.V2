from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QColorDialog, QSlider, QHBoxLayout
from PySide6.QtCore import Qt
from core.character_system.character_system import CharacterSystem

class MaterialEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🎨 Material-Editor"))

        self.material_selector = QComboBox()
        self.material_selector.addItems(["skin", "clothes", "piercings", "tattoos"])
        layout.addWidget(QLabel("Material auswählen:"))
        layout.addWidget(self.material_selector)

        self.color_btn = QPushButton("Farbe wählen")
        self.color_btn.clicked.connect(self.choose_color)
        layout.addWidget(self.color_btn)

        layout.addWidget(QLabel("Roughness"))
        self.rough_slider = QSlider(Qt.Horizontal)
        self.rough_slider.setRange(0, 100)
        self.rough_slider.setValue(50)
        self.rough_slider.valueChanged.connect(self.set_roughness)
        layout.addWidget(self.rough_slider)

        layout.addWidget(QLabel("Metallic"))
        self.metal_slider = QSlider(Qt.Horizontal)
        self.metal_slider.setRange(0, 100)
        self.metal_slider.setValue(0)
        self.metal_slider.valueChanged.connect(self.set_metallic)
        layout.addWidget(self.metal_slider)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            mat = self.material_selector.currentText()
            self.character_system.set_material_color(mat, color.name())

    def set_roughness(self, val):
        mat = self.material_selector.currentText()
        self.character_system.set_material_value(mat, "roughness", val / 100.0)

    def set_metallic(self, val):
        mat = self.material_selector.currentText()
        self.character_system.set_material_value(mat, "metallic", val / 100.0)