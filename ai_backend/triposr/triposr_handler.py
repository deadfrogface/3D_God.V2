import os
import subprocess

def image_to_mesh(image_path: str, output_dir: str = "output", resolution: int = 512) -> bool:
    """
    Führt TripoSR aus und generiert eine 3D-Mesh-Datei aus einem Bild.

    :param image_path: Pfad zum Eingabebild (.png, .jpg)
    :param output_dir: Zielordner für Ausgabe-Meshes (z. B. .ply/.obj)
    :param resolution: Zielauflösung (Standard: 512x512)
    :return: True bei Erfolg, False bei Fehler
    """

    # Pfad zum umbenannten Inferenzskript (run.py → triposr_run.py)
    script_path = os.path.join(os.path.dirname(__file__), "triposr_run.py")

    if not os.path.exists(script_path):
        print("❌ Fehler: triposr_run.py nicht gefunden.")
        return False

    if not os.path.exists(image_path):
        print("❌ Fehler: Eingabebild nicht gefunden.")
        return False

    print("📦 Starte TripoSR-Inferenz ...")

    # Starte TripoSR-Inferenz via subprocess
    result = subprocess.run([
        "python", script_path,
        image_path,
        "--output-dir", output_dir,
        "--resolution", str(resolution)
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Fehler bei TripoSR:")
        print(result.stderr)
        return False

    print("✅ Mesh wurde generiert und gespeichert in:", output_dir)
    return True
