import bpy
import json
import os

bones = []
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        for bone in obj.data.bones:
            bones.append(bone.name)

output_path = os.path.join("exports", "last_bone_export.json")
with open(output_path, "w") as f:
    json.dump(bones, f, indent=4)

print(f"[Export] {len(bones)} Bones gespeichert unter {output_path}")