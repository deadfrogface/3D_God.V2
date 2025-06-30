import bpy
import os

# Lese Zielpfad aus Umgebungsvariable
export_path = os.environ.get("FBX_EXPORT_PATH", "character_export.fbx")

print(f"[Blender Script] Exportiere FBX nach: {export_path}")

# Exportiere alles in der Szene
bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=False,
    apply_unit_scale=True,
    bake_space_transform=True
)

print("[Blender Script] Export abgeschlossen.")