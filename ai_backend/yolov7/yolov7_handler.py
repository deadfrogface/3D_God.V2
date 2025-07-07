import os
import subprocess

def detect_objects(image_path: str, output_dir: str = "runs/detect", conf_threshold: float = 0.25) -> bool:
    """
    Führt YOLOv7-Objekterkennung auf einem Bild aus.

    :param image_path: Pfad zum Eingabebild
    :param output_dir: Zielordner für Ergebnisse (optional)
    :param conf_threshold: Confidence Threshold (Standard: 0.25)
    :return: True bei Erfolg, False bei Fehler
    """
    yolov7_script = os.path.join(os.path.dirname(__file__), "yolov7_detect.py")
    weights_path = os.path.join(os.path.dirname(__file__), "yolov7.pt")

    if not os.path.exists(yolov7_script):
        print("❌ Fehler: yolov7_detect.py nicht gefunden.")
        return False

    if not os.path.exists(weights_path):
        print("❌ Fehler: yolov7.pt nicht gefunden.")
        return False

    print("🔎 Starte YOLOv7 Objekterkennung ...")

    result = subprocess.run([
        "python", yolov7_script,
        "--weights", weights_path,
        "--source", image_path,
        "--conf", str(conf_threshold),
        "--project", output_dir,
        "--save-txt",
        "--save-conf"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ YOLOv7-Fehler:")
        print(result.stderr)
        return False

    print("✅ Objekterkennung abgeschlossen.")
    return True
