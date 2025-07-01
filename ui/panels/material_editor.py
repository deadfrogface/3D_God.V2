from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QColorDialog,
    QSlider, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from core.character_system.character_system import CharacterSystem
import os

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

        self.texture_preview = QLabel("Keine Textur gewählt")
        self.texture_preview.setFixedHeight(100)
        self.texture_preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.texture_preview)

        self.texture_btn = QPushButton("Textur auswählen")
        self.texture_btn.clicked.connect(self.choose_texture)
        layout.addWidget(self.texture_btn)

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

    def choose_texture(self):
        path, _ = QFileDialog.getOpenFileName(self, "Textur auswählen", "", "Bilder (*.png *.jpg *.jpeg)")
        if path:
            mat = self.material_selector.currentText()
            self.character_system.set_material_texture(mat, path)
            pix = QPixmap(path).scaledToHeight(100, Qt.SmoothTransformation)
            self.texture_preview.setPixmap(pix)
            self.texture_preview.setText("")