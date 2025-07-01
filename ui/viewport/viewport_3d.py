from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Viewport3D(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("🔲 [3D Vorschau hier – Platzhalter]")
        self.label.setStyleSheet("background-color: #222; color: white; padding: 30px;")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_preview(self, anatomy_state, asset_state):
        text = "🔎 Live-Vorschau:\n"
        text += "\n🧬 Anatomie:\n"
        for k, v in anatomy_state.items():
            if v:
                text += f" ✅ {k}\n"
        text += "\n🧩 Assets:\n"
        for k, items in asset_state.items():
            for i in items:
                text += f" • {k}: {i}\n"
        self.label.setText(text)

    def load_animation(self, name):
        print(f"[Viewport3D] Animation geladen: {name} (simuliert)")
        self.label.setText(f"▶ Animation: {name}")

    def stop_animation(self):
        self.label.setText("🔲 [3D Vorschau hier – Platzhalter]")

    def show_materials(self, materials):
        text = "🎨 Materialien aktiv:\n"
        for name, mat in materials.items():
            text += f"• {name} → {mat['color']}\n"
        self.label.setText(text)