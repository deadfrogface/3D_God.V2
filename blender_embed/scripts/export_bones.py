import bpy
import json
import os

print("[Rig][ExportBones] ▶️ Starte Bone-Export")

bones = []
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        for bone in obj.data.bones:
            bones.append(bone.name)
        print(f"[Rig][ExportBones] ✅ Armature gefunden: {obj.name} mit {len(obj.data.bones)} Bones")

output_path = os.path.join("exports", "last_bone_export.json")
try:
    with open(output_path, "w") as f:
        json.dump(bones, f, indent=4)
    print(f"[Rig][ExportBones] ✅ {len(bones)} Bones gespeichert unter: {output_path}")
except Exception as e:
    print(f"[Rig][ExportBones] ❌ Fehler beim Speichern: {e}")