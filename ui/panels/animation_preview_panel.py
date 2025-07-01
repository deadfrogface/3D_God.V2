from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from core.character_system.character_system import CharacterSystem

class AnimationPreviewPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.character_system = CharacterSystem()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🎬 Animation Vorschau"))

        self.anim_select = QComboBox()
        self.anim_select.addItems(["Idle", "Walk", "Run", "CombatIdle", "Pose_A", "Pose_B"])
        layout.addWidget(self.anim_select)

        btn_play = QPushButton("▶ Animation abspielen")
        btn_play.clicked.connect(self.play_animation)
        layout.addWidget(btn_play)

        btn_stop = QPushButton("⏹ Stop")
        btn_stop.clicked.connect(self.stop_animation)
        layout.addWidget(btn_stop)

        self.setLayout(layout)

    def play_animation(self):
        selected = self.anim_select.currentText()
        self.character_system.play_animation(selected)

    def stop_animation(self):
        self.character_system.stop_animation()