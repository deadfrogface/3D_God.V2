import shutil, os

def export_to_ue(model_path):
    export_dir = "exports/ue_models"
    os.makedirs(export_dir, exist_ok=True)
    shutil.copy(model_path, export_dir)
    print(f"Exportiert nach {export_dir}")
