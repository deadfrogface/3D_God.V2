import subprocess
import json

def open_blender_sculpt(file_path):
    with open('config.json') as config_file:
        config = json.load(config_file)
        blender_exe = config['blender_path']
    subprocess.run([blender_exe, file_path])

