import bpy
import os

def export_fbx(output_path="exports/final_model.fbx"):
    print("[Export] Starte FBX-Export...")
    
    # Wähle alle sichtbaren Objekte
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type in ['MESH', 'ARMATURE']:
            obj.select_set(True)
    
    # Exportiere alles
    bpy.ops.export_scene.fbx(
        filepath=output_path,
        use_selection=True,
        apply_unit_scale=True,
        bake_space_transform=True,
        object_types={'MESH', 'ARMATURE'},
        add_leaf_bones=False,
        path_mode='COPY',
        embed_textures=True
    )
    
    print(f"[Export] FBX erfolgreich gespeichert unter: {output_path}")