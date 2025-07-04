import bpy
import os
from core.logger import log

def export_fbx(output_path="exports/final_model.fbx"):
    log.info("[ExportFBX][export_fbx] ▶️ Starte FBX-Export...")

    try:
        # Auswahl zurücksetzen
        bpy.ops.object.select_all(action='DESELECT')
        log.debug("[ExportFBX][export_fbx] ▶️ Alle Objekte abgewählt")

        # MESH & ARMATURE Objekte selektieren
        selected = 0
        for obj in bpy.data.objects:
            if obj.type in ['MESH', 'ARMATURE']:
                obj.select_set(True)
                selected += 1

        log.success(f"[ExportFBX][export_fbx] ✅ {selected} Objekte zur Auswahl hinzugefügt")

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

        log.success(f"[ExportFBX][export_fbx] ✅ FBX erfolgreich gespeichert unter: {output_path}")

    except Exception as e:
        log.error(f"[ExportFBX][export_fbx] ❌ Fehler beim Export: {e}")