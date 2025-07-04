import bpy
import sys
import json
import os

print("[Export][FBX] ▶️ Starte Export-Prozess")

args = sys.argv
output_name = "exported_character"
if "--" in args:
    idx = args.index("--")
    if idx + 1 < len(args):
        output_name = args[idx + 1]

export_path = os.path.join("exports", f"{output_name}.fbx")
preset_path = os.path.join("presets", f"{output_name}.json")

print(f"[Export][FBX] 📁 Zielpfad: {export_path}")
print(f"[Export][FBX] 📖 Lade Preset: {preset_path}")

materials = {}
if os.path.exists(preset_path):
    with open(preset_path, "r") as f:
        data = json.load(f)
        materials = data.get("materials", {})
        print("[Export][FBX] ✅ Preset geladen.")
else:
    print("[Export][FBX] ⚠️ Kein Preset gefunden – verwende Standardfarben.")

def apply_material(obj, mat_data):
    if obj.type != 'MESH':
        return
    mat = bpy.data.materials.new(name="Material_" + obj.name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        hex_color = mat_data.get("color", "#cccccc").lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1)
        bsdf.inputs["Roughness"].default_value = mat_data.get("roughness", 0.5)
        bsdf.inputs["Metallic"].default_value = mat_data.get("metallic", 0.0)

    tex_path = mat_data.get("texture", "")
    if tex_path and os.path.exists(tex_path):
        tex_image = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_image.image = bpy.data.images.load(tex_path)
        mat.node_tree.links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
        print(f"[Export][Material] 🎨 Textur geladen: {tex_path}")

    obj.data.materials.clear()
    obj.data.materials.append(mat)
    print(f"[Export][Material] ✅ Material angewendet auf: {obj.name}")

bpy.ops.object.select_all(action='SELECT')

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

# Bone-Mapping für UE5 / Metahuman
bone_rename_map = {
    "spine": "spine_01",
    "head": "head",
    "nipple.L": "nipple_l",
    "nipple.R": "nipple_r",
    "genital": "pelvis_attachment",
    "cloth_back": "coat_back",
    "piercing_nose": "nose_piercing"
}

for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        for bone in obj.data.bones:
            if bone.name in bone_rename_map:
                print(f"[Export][BoneMap] 🔁 {bone.name} → {bone_rename_map[bone.name]}")
                bone.name = bone_rename_map[bone.name]

try:
    bpy.ops.export_scene.fbx(
        filepath=export_path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL',
        bake_space_transform=True,
        object_types={'ARMATURE', 'MESH'},
        use_armature_deform_only=True
    )
    print(f"[Export][FBX] ✅ Export abgeschlossen: {export_path}")
except Exception as e:
    print(f"[Export][FBX] ❌ Fehler beim Export: {e}")