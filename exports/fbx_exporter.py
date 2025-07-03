import bpy
import os

def export_fbx(output_path="exports/final_model.fbx"):
    print("[ExportFBX][export_fbx] ▶️ Starte FBX-Export...")

    try:
        # Auswahl zurücksetzen
        bpy.ops.object.select_all(action='DESELECT')
        print("[ExportFBX][export_fbx] ▶️ Alle Objekte abgewählt")

        # MESH & ARMATURE Objekte selektieren
        selected = 0
        for obj in bpy.data.objects:
            if obj.type in ['MESH', 'ARMATURE']:
                obj.select_set(True)
                selected += 1

        print(f"[ExportFBX][export_fbx] ✅ {selected} Objekte zur Auswahl hinzugefügt")

        # Export durchführen
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

        print(f"[ExportFBX][export_fbx] ✅ FBX erfolgreich gespeichert unter: {output_path}")

    except Exception as e:
        print(f"[ExportFBX][export_fbx] ❌ Fehler beim Export: {e}")