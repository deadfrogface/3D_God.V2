import bpy
import os

# Deaktiviere Kamera & Licht
for obj in bpy.data.objects:
    if obj.type in {'CAMERA', 'LIGHT'}:
        obj.hide_render = True
        obj.hide_viewport = True

# Alles selektieren und FBX exportieren
bpy.ops.object.select_all(action='SELECT')

export_path = os.environ.get("FBX_EXPORT_PATH", "C:/Temp/output.fbx")
print(f"📤 Exportiere FBX nach: {export_path}")

bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=True,
    apply_scale_options='FBX_SCALE_UNITS',
    object_types={'MESH', 'ARMATURE'},
    bake_space_transform=True,
    axis_forward='-Z',
    axis_up='Y'
)