from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.info_label = QLabel("🔲 [3D Vorschau hier – Placeholder]")
        self.info_label.setStyleSheet("background-color: #222; color: white; padding: 40px;")
        layout.addWidget(self.info_label)
        self.setLayout(layout)

    def update_preview(self, anatomy_state, asset_state):
        print("[Viewport3D] Preview aktualisiert")
        print(" - Anatomie:", anatomy_state)
        print(" - Assets:", asset_state)

    def load_animation(self, name):
        print(f"[Viewport3D] Animation geladen: {name} (simuliert)")
        self.info_label.setText(f"▶ Animation: {name}")

    def stop_animation(self):
        print("[Viewport3D] Animation gestoppt.")
        self.info_label.setText("🔲 [3D Vorschau hier – Placeholder]")