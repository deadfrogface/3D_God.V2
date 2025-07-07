# Auto-Installer für OpenCV
try:
    import cv2
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2  # nachinstallieren

import os

def load_image(image_path: str):
    """Lädt ein Bild und gibt ein OpenCV-Array zurück."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Bild nicht gefunden: {image_path}")
    return cv2.imread(image_path)

def save_image(image, output_path: str):
    """Speichert ein OpenCV-Bild."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)

def crop_image(image, x: int, y: int, width: int, height: int):
    """Schneidet ein Bild auf die gewünschte Region zu."""
    return image[y:y+height, x:x+width]

def convert_to_grayscale(image):
    """Wandelt ein Farbbild in ein Graustufenbild um."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_image(image, width: int, height: int):
    """Skaliert ein Bild auf die gewünschte Größe."""
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def draw_bbox(image, bbox, color=(0, 255, 0), thickness=2):
    """Zeichnet eine Bounding Box ins Bild. bbox = (x, y, w, h)"""
    x, y, w, h = bbox
    return cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness)
