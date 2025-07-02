import bpy
import json
import os

# 🚪 Eingabepfad
input_path = os.path.join(os.path.dirname(__file__), "sculpt_input.json")
glb_output = os.path.abspath("exports/preview.glb")
blend_path = os.path.join(os.path.dirname(__file__), "base_model.blend")

print("[Blender] Lade sculpt_input.json...")
with open(input_path, "r") as f:
    data = json.load(f)

# 🔁 Blender-Datei öffnen
print("[Blender] Öffne base_model.blend...")
bpy.ops.wm.open_mainfile(filepath=blend_path)

obj = bpy.data.objects.get("Body")
if not obj:
    print("[Blender] Objekt 'Body' nicht gefunden!")
    exit()

bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')

# 📏 Beispiel-Modifikationen (einfach skaliert auf Y-Achse)
def apply_sculpt(param, factor, axis='Y'):
    if axis == 'X': idx = 0
    elif axis == 'Z': idx = 2
    else: idx = 1

    scale = 1 + ((factor - 50) / 50) * 0.5
    print(f"[Sculpt] {param} → scale[{axis}] = {scale}")
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(1,1,1))  # Reset-Sicherheit

    for v in obj.data.vertices:
        co = v.co[idx]
        if param == "height" and idx == 2:
            v.co[idx] *= scale
        elif param == "breast_size" and v.co[0] > 0.2:
            v.co[idx] *= scale
        elif param == "hip_width" and v.co[2] < 0.5:
            v.co[idx] *= scale

bpy.ops.object.mode_set(mode='OBJECT')

# 📊 Werte anwenden
apply_sculpt("height", data.get("height", 50), axis='Z')
apply_sculpt("breast_size", data.get("breast_size", 50), axis='Y')
apply_sculpt("hip_width", data.get("hip_width", 50), axis='X')

# 💾 Export als .glb
print(f"[Blender] Exportiere Vorschau: {glb_output}")
bpy.ops.export_scene.gltf(filepath=glb_output, export_format='GLB')

print("[Blender] Sculpt abgeschlossen.")