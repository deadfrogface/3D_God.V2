import json  
import subprocess  
import os  

class SculptTools:  
    def __init__(self):  
        self.input_path = "blender_embed/sculpt_input.json"  
        self.script_path = "blender_embed/sculpt_main.py"  
        self.blender_path = self.get_blender_path()  

    def get_blender_path(self):  
        try:  
            with open("config.json") as config_file:  
                config = json.load(config_file)  
                return config.get("blender_path", "blender.exe")  
        except Exception as e:  
            print(f"[SculptBridge] Fehler beim Lesen der config.json: {e}")  
            return "blender.exe"  

    def send_data(self, sculpt_data):  
        os.makedirs(os.path.dirname(self.input_path), exist_ok=True)  
        with open(self.input_path, "w") as f:  
            json.dump(sculpt_data, f, indent=4)  
        print(f"[SculptBridge] Daten geschrieben → {self.input_path}")  

    def launch(self):  
        if not os.path.exists(self.blender_path):  
            print(f"[SculptBridge] Fehler: Blender nicht gefunden unter {self.blender_path}")  
            return  

        abs_script_path = os.path.abspath(self.script_path)  
        cmd = [  
            self.blender_path,  
            "--background",  
            "--python", abs_script_path  
        ]  
        print(f"[SculptBridge] Starte Blender mit:\n{' '.join(cmd)}")  
        subprocess.Popen(cmd)