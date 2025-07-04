import bpy
import json
import os

print("[SculptMain] ▶️ Starte Sculpt-Template...")

data_path = os.path.join("blender_embed", "sculpt_input.json")
if not os.path.exists(data_path):
    print("[SculptMain] ❌ Keine Sculpt-Daten gefunden unter:", data_path)
    bpy.ops.wm.quit_blender()

print(f"[SculptMain] ▶️ Lade Datei: {data_path}")
try:
    with open(data_path, "r") as f:
        sculpt_data = json.load(f)
    print("[SculptMain] ✅ Eingeladene Daten:", sculpt_data)
except Exception as e:
    print(f"[SculptMain] ❌ Fehler beim Laden der Daten: {e}")
    bpy.ops.wm.quit_blender()

# 🔢 Skalierung berechnen
scale_factor = sculpt_data.get("height", 50) / 50
print(f"[SculptMain] ▶️ Wende Skalierungsfaktor an: {scale_factor:.2f}")

for obj in bpy.data.objects:
    if obj.type == "MESH":
        obj.scale = (scale_factor, scale_factor, scale_factor)
        print(f"[SculptMain] ✅ Skaliert: {obj.name}")

# 🎨 Sculpt-Modus aktivieren
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')
        print(f"[SculptMain] ✅ Sculpt-Modus aktiviert für: {obj.name}")
        break

print("[SculptMain] ✅ Vorgang abgeschlossen.")