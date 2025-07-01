import bpy
import sys
import json
import os

# Argumente ab "--"
args = sys.argv
output_name = "exported_character"
if "--" in args:
    idx = args.index("--")
    if idx + 1 < len(args):
        output_name = args[idx + 1]

export_path = os.path.join("exports", f"{output_name}.fbx")
preset_path = os.path.join("presets", f"{output_name}.json")

print(f"[Export] Zielpfad: {export_path}")
print(f"[Export] Lade Preset: {preset_path}")

# Materialien laden
materials = {}
if os.path.exists(preset_path):
    with open(preset_path, "r") as f:
        data = json.load(f)
        materials = data.get("materials", {})
else:
    print("[Export] Kein Preset gefunden – verwende Standardwerte.")

# Helper: Material setzen
def apply_material(obj, mat_data):
    if obj.type != 'MESH':
        return
    mat = bpy.data.materials.new(name="Material_" + obj.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        # Farbe setzen
        hex_color = mat_data.get("color", "#cccccc").lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1)

        # Roughness / Metallic
        bsdf.inputs["Roughness"].default_value = mat_data.get("roughness", 0.5)
        bsdf.inputs["Metallic"].default_value = mat_data.get("metallic", 0.0)

    obj.data.materials.clear()
    obj.data.materials.append(mat)
    print(f"[Material] Zugewiesen an {obj.name}")

# Auswahl vorbereiten
bpy.ops.object.select_all(action='SELECT')

# Materialien anwenden basierend auf Objektnamen
for obj in bpy.context.selected_objects:
    name = obj.name.lower()
    if "skin" in name:
        apply_material(obj, materials.get("skin", {}))
    elif "clothes" in name:
        apply_material(obj, materials.get("clothes", {}))
    elif "piercing" in name:
        apply_material(obj, materials.get("piercings", {}))
    elif "tattoo" in name:
        apply_material(obj, materials.get("tattoos", {}))

# Exportieren
bpy.ops.export_scene.fbx(filepath=export_path, use_selection=True)
print(f"[Export] FBX gespeichert: {export_path}")