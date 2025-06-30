import bpy
import os

export_path = os.environ.get("FBX_EXPORT_PATH", "exports/character.fbx")
print(f"[Blender Export] Exportiere nach: {export_path}")

# Optional: alles auswählen
for obj in bpy.data.objects:
    obj.select_set(True)

# Exportieren als FBX
bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=True,
    apply_unit_scale=True,
    bake_space_transform=True,
    object_types={'ARMATURE', 'MESH'},
    use_armature_deform_only=True,
    add_leaf_bones=False,
    axis_forward='-Z',
    axis_up='Y'
)

print("[Blender Export] ✅ Export abgeschlossen")