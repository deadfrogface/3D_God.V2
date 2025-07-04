import bpy

print("[Rig][AutoRig] ▶️ Starte Auto-Rig-Prozess")

try:
    # Existierende Armatures entfernen
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            obj.select_set(True)
    bpy.ops.object.delete()

    # Neue Armature hinzufügen
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    arm = bpy.context.active_object
    arm.name = "AutoRig"
    bpy.ops.object.mode_set(mode='EDIT')

    edit_bones = arm.data.edit_bones

    def create_bone(name, head, tail):
        bone = edit_bones.new(name)
        bone.head = head
        bone.tail = tail
        print(f"[Rig][AutoRig] ➕ Knochen erstellt: {name}")
        return bone

    # Basisknochen
    create_bone("spine", (0, 0, 1), (0, 0, 2))
    create_bone("head", (0, 0, 2), (0, 0, 2.5))

    # Extra-Bones
    create_bone("nipple.L", (0.1, 0.3, 1.5), (0.1, 0.3, 1.55))
    create_bone("nipple.R", (-0.1, 0.3, 1.5), (-0.1, 0.3, 1.55))
    create_bone("genital", (0, 0.1, 1), (0, 0.1, 0.8))
    create_bone("cloth_back", (0, -0.2, 1.8), (0, -0.2, 1.2))
    create_bone("piercing_nose", (0, 0.1, 2.1), (0, 0.1, 2.15))

    bpy.ops.object.mode_set(mode='OBJECT')
    print("[Rig][AutoRig] ✅ Rig erstellt: AutoRig")

except Exception as e:
    print(f"[Rig][AutoRig] ❌ Fehler beim Auto-Rigging: {e}")