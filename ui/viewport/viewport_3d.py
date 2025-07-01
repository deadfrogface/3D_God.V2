from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("🔲 [3D Vorschau hier – Placeholder]")
        self.label.setStyleSheet("background-color: #222; color: white; padding: 40px;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_preview(self, anatomy_state, asset_state):
        print("[Viewport3D] Preview aktualisiert")
        print(" - Anatomie:", anatomy_state)
        print(" - Assets:", asset_state)

    def load_animation(self, name):
        print(f"[Viewport3D] Animation geladen: {name} (simuliert)")
        self.label.setText(f"▶ Animation: {name}")

    def stop_animation(self):
        print("[Viewport3D] Animation gestoppt.")
        self.label.setText("🔲 [3D Vorschau hier – Placeholder]")

    def show_materials(self, materials):
        self.label.setText("🎨 Materialien aktiv:\n")
        for name, mat in materials.items():
            self.label.setText(self.label.text() + f"• {name} → {mat['color']}\n")