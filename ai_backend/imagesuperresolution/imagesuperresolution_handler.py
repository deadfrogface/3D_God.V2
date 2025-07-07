import os
import subprocess

def upscale_image(input_path: str, output_path: str = None, model_name: str = "RealESRGAN_x4plus") -> bool:
    """
    Skaliert ein Bild mit Real-ESRGAN hoch (Super-Resolution).

    :param input_path: Pfad zum Bild (.png/.jpg), das verbessert werden soll
    :param output_path: Optionaler Pfad zum Zielbild
    :param model_name: Modellname (z. B. RealESRGAN_x4plus, RealESRGAN_x4plus_anime_6B)
    :return: True bei Erfolg, False bei Fehler
    """
    script_path = os.path.join(os.path.dirname(__file__), "inference_realesrgan.py")

    if not os.path.exists(script_path):
        print("❌ Fehler: inference_realesrgan.py nicht gefunden.")
        return False

    if not os.path.exists(input_path):
        print("❌ Fehler: Eingabebild nicht gefunden.")
        return False

    if output_path is None:
        output_path = os.path.join("output", os.path.basename(input_path))

    print("🎨 Starte Bildvergrößerung mit Real-ESRGAN ...")

    result = subprocess.run([
        "python", script_path,
        "-n", model_name,
        "-i", input_path,
        "-o", output_path
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Fehler bei Super-Resolution:")
        print(result.stderr)
        return False

    print("✅ Bild erfolgreich hochskaliert:", output_path)
    return True
