from ai_modules.triposr.triposr_handler import TripoSRHandler
from ai_modules.juggernaut.juggernaut_handler import JuggernautHandler
from pathlib import Path
import os

class AIGenerator:
    def __init__(self, config):
        self.config = config
        self.triposr = TripoSRHandler()
        self.juggernaut = JuggernautHandler()
        self.export_dir = Path("exports/generated")
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, text_prompt: str, image_path: str, asset_type: str):
        if image_path:
            print("🖼️ Starte Bild → 3D via TripoSR...")
            return self.triposr.generate_from_image(image_path)

        elif text_prompt:
            print(f"✏️ Starte Text → Bild für '{text_prompt}'...")
            temp_img_path = self.export_dir / "temp_ref.png"
            ref_path = self.juggernaut.generate_reference_image(text_prompt, str(temp_img_path))

            print(f"🧊 Starte TripoSR mit Referenzbild...")
            return self.triposr.generate_from_image(ref_path)

        else:
            raise ValueError("Kein Text oder Bild angegeben zur Generierung.")