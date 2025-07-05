from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from core.character_system.character_system import CharacterSystem
from core.logger import log

class AnimationPreviewPanel(QWidget):
    def __init__(self, character_system: CharacterSystem):
        try:
            super().__init__()
            self.character_system = character_system
            log.info("[AnimationPreviewPanel][__init__] ▶️ Initialisiere Animation-Panel...")

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
            log.info("[AnimationPreviewPanel][__init__] ✅ Panel bereit")
        except Exception as e:
            log.error(f"[AnimationPreviewPanel][__init__] ❌ Fehler bei Initialisierung: {e}")
            raise

    def play_animation(self):
        selected = self.anim_select.currentText()
        try:
            log.info(f"[AnimationPreviewPanel][play_animation] ▶️ Spiele Animation: {selected}")
            self.character_system.play_animation(selected)
        except Exception as e:
            log.error(f"[AnimationPreviewPanel][play_animation] ❌ Fehler: {e}")

    def stop_animation(self):
        try:
            log.info("[AnimationPreviewPanel][stop_animation] ⏹ Stoppe Animation")
            self.character_system.stop_animation()
        except Exception as e:
            log.error(f"[AnimationPreviewPanel][stop_animation] ❌ Fehler: {e}")