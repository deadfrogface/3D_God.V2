import bpy
import os

# Zielpfad über Umgebungsvariable lesen
export_path = os.environ.get("FBX_EXPORT_PATH", "C:/Temp/exported_character.fbx")

print(f"📦 Exportiere Szene als FBX nach: {export_path}")

# Alles selektieren
bpy.ops.object.select_all(action='SELECT')

# FBX exportieren
bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=True,
    apply_unit_scale=True,
    global_scale=1.0,
    apply_scale_options='FBX_SCALE_ALL',
    object_types={'ARMATURE', 'MESH'},
    bake_space_transform=True
)

print("✅ FBX-Export abgeschlossen")