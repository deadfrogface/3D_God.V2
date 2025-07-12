# ui/viewport/viewport_3d.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from core.logger import log

# 🔧 Automatische Installation (wenn nötig)
try:
    import trimesh
    import pyrender
    import numpy as np
    from PySide6.QtGui import QImage, QPainter
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyrender", "PyOpenGL", "trimesh", "numpy"])
    import trimesh
    import pyrender
    import numpy as np
    from PySide6.QtGui import QImage, QPainter

import os

class GLBViewport(QOpenGLWidget):
    def __init__(self, glb_path, parent=None):
        super().__init__(parent)
        self.glb_path = glb_path
        self.scene = None
        self.img = None

    def showEvent(self, event):
        super().showEvent(event)
        self.load_glb(self.glb_path)

    def initializeGL(self):
        pass  # Wichtiger Fix: GL wird erst in showEvent geladen

    def load_glb(self, path):
        if not os.path.exists(path):
            log.error(f"[GLBViewport] ❌ Datei nicht gefunden: {path}")
            return
        log.info(f"[GLBViewport] ▶️ Lade Modell: {path}")

        try:
            mesh = trimesh.load(path, force='mesh')
            if isinstance(mesh, trimesh.Scene):
                mesh = mesh.dump().sum()

            render_mesh = pyrender.Mesh.from_trimesh(mesh, smooth=True)
            scene = pyrender.Scene()
            scene.add(render_mesh)

            cam = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
            scene.add(cam, pose=np.eye(4))
            light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
            scene.add(light, pose=np.eye(4))

            r = pyrender.OffscreenRenderer(self.width(), self.height())
            color, _ = r.render(scene)
            self.img = color
            self.update()
            log.success(f"[GLBViewport] ✅ Modell gerendert")
        except Exception as e:
            log.error(f"[GLBViewport] ❌ Rendering-Fehler: {e}")

    def paintGL(self):
        if self.img is None:
            return
        image = QImage(self.img, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888)
        painter = QPainter(self)
        painter.drawImage(0, 0, image)
        painter.end()

    def resizeGL(self, w, h):
        self.load_glb(self.glb_path)


class Viewport3D(QWidget):
    def __init__(self, character_system):
        super().__init__()
        log.info("[Viewport3D][__init__] ▶️ Initialisiere Viewport...")
        self.character_system = character_system
        self.character_system.bind_viewport(self)

        self.current_path = "assets/characters/male_base.glb"

        layout = QVBoxLayout()
        title = QLabel("🖼️ 3D Vorschau")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.glb_widget = GLBViewport(self.current_path)
        layout.addWidget(self.glb_widget)

        layout.addStretch()
        self.setLayout(layout)
        log.success("[Viewport3D][__init__] ✅ Viewport bereit")

    def update_view(self):
        log.info("[Viewport3D][update_view] ▶️ Aktualisiere Modell")
        self.glb_widget.load_glb(self.current_path)

    def update_preview(self, anatomy_state=None, asset_state=None):
        log.info("[Viewport3D][update_preview] 🌀 Aktualisiere 3D-Vorschau (anatomy/assets)")
        self.update_view()

    def load_preview(self, path):
        log.info(f"[Viewport3D][load_preview] 📥 Lade Vorschau aus Pfad: {path}")
        if os.path.exists(path):
            self.current_path = path
            self.glb_widget.glb_path = path
            self.glb_widget.load_glb(path)
            log.success("[Viewport3D][load_preview] ✅ Modell geladen")
        else:
            log.error(f"[Viewport3D][load_preview] ❌ Pfad nicht gefunden: {path}")
