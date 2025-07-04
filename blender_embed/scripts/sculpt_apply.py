import bpy
import json
import os

print("[Blender] Starte Sculpt-Template...")

data_path = os.path.join("blender_embed", "sculpt_input.json")
if not os.path.exists(data_path):
    print("[Blender] Keine Sculpt-Daten gefunden.")
    bpy.ops.wm.quit_blender()

with open(data_path, "r") as f:
    sculpt_data = json.load(f)

print("[Blender] Eingeladene Daten:", sculpt_data)

# Beispiel: Größe skalieren
scale_factor = sculpt_data.get("height", 50) / 50
for obj in bpy.data.objects:
    if obj.type == "MESH":
        obj.scale = (scale_factor, scale_factor, scale_factor)

# Sculpt-Modus aktivieren
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')
        break
