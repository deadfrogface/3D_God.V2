import bpy
import json
import os

# 🔁 Pfade definieren
base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "sculpt_input.json")
blend_path = os.path.join(base_dir, "base_model.blend")
glb_output = os.path.abspath("exports/preview.glb")

# 📥 JSON laden
print("[Blender] Lade Eingabedaten...")
with open(input_path, "r") as f:
    data = json.load(f)

# 📂 .blend-Datei öffnen
print("[Blender] Lade:", blend_path)
bpy.ops.wm.open_mainfile(filepath=blend_path)

# 🧍 Objekt auswählen
obj = bpy.data.objects.get("Body")
if not obj:
    print("[Blender] Fehler: Objekt 'Body' nicht gefunden!")
    exit()

bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')

def apply_sculpt(param, factor, axis='Y'):
    if axis == 'X': idx = 0
    elif axis == 'Z': idx = 2
    else: idx = 1

    scale = 1 + ((factor - 50) / 50) * 0.5
    print(f"[Sculpt] {param}: Skaliere {axis} mit Faktor {scale:.2f}")

    bpy.ops.mesh.select_all(action='SELECT')
    for v in obj.data.vertices:
        co = v.co[idx]
        if param == "height" and idx == 2:
            v.co[idx] *= scale
        elif param == "breast_size" and v.co[0] > 0.2:
            v.co[idx] *= scale
        elif param == "hip_width" and v.co[2] < 0.5:
            v.co[idx] *= scale

bpy.ops.object.mode_set(mode='OBJECT')

# 🧠 Sculpting anwenden
apply_sculpt("height", data.get("height", 50), axis='Z')
apply_sculpt("breast_size", data.get("breast_size", 50), axis='Y')
apply_sculpt("hip_width", data.get("hip_width", 50), axis='X')

# 🔁 Symmetrie aktivieren?
if data.get("symmetry", True):
    print("[Blender] Wende X-Symmetrie an")
    bpy.context.tool_settings.use_mesh_mirror_x = True
else:
    bpy.context.tool_settings.use_mesh_mirror_x = False

# 💾 Vorschau speichern
print(f"[Blender] Exportiere Vorschau als GLB → {glb_output}")
bpy.ops.export_scene.gltf(filepath=glb_output, export_format='GLB')

print("[Blender] Fertig.")