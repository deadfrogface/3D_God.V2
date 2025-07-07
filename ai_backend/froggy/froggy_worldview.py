import os
import json
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CACHE_PATH = os.path.join(os.path.dirname(__file__), "worldview_cache.json")

def scan_worldview():
    """
    Scannt das 3D_God Projektverzeichnis und erfasst die Weltstruktur.
    Gibt ein Dict mit Pfaden, Dateitypen, Erkennungen und Modulstatus zurück.
    """
    worldview = {
        "timestamp": datetime.utcnow().isoformat(),
        "paths": [],
        "modules": {},
        "missing": [],
        "stats": {
            "total_files": 0,
            "py_files": 0,
            "images": 0,
            "models": 0
        }
    }

    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)
            worldview["paths"].append(rel_path)
            worldview["stats"]["total_files"] += 1

            if file.endswith(".py"):
                worldview["stats"]["py_files"] += 1
            elif file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                worldview["stats"]["images"] += 1
            elif file.endswith((".pt", ".ckpt", ".obj", ".fbx")):
                worldview["stats"]["models"] += 1

    # Prüfe bekannte KI-Module
    required_modules = {
        "yolov7": "ai_backend/yolov7/yolov7_handler.py",
        "triposr": "ai_backend/triposr/triposr_handler.py",
        "superres": "ai_backend/imagesuperresolution/imagesuperresolution_handler.py",
        "charmorph": "ai_backend/charmorph/charmorph_handler.py",
        "fauxpilot": "ai_backend/fauxpilot/fauxpilot_server.py"
    }

    for name, path in required_modules.items():
        worldview["modules"][name] = os.path.exists(os.path.join(PROJECT_ROOT, path))
        if not worldview["modules"][name]:
            worldview["missing"].append(path)

    # Speichern
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(worldview, f, indent=2)

    return worldview

def get_cached_worldview():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
