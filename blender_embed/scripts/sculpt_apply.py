import bpy
import json
import os

# 🔁 Pfade definieren
base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "sculpt_input.json")
blend_path = os.path.join(base_dir, "base_model.blend")
glb_output = os.path.abspath("exports/preview.glb")
preview_img_path = os.path.abspath("exports/preview.png")

print("[SculptMain] ▶️ Start")

# 📥 JSON laden
print("[SculptMain] ▶️ Lade Eingabedaten...")
try:
    with open(input_path, "r") as f:
        data = json.load(f)
    print(f"[SculptMain] ✅ Daten geladen: {data}")
except Exception as e:
    print(f"[SculptMain] ❌ Fehler beim Laden der Eingabedatei: {e}")
    exit(1)

# 📂 .blend-Datei öffnen
print(f"[SculptMain] ▶️ Lade .blend Datei: {blend_path}")
if not os.path.exists(blend_path):
    print(f"[SculptMain] ❌ base_model.blend nicht gefunden unter: {blend_path}")
    exit(1)
bpy.ops.wm.open_mainfile(filepath=blend_path)

# 🧍 Objekt auswählen
obj = bpy.data.objects.get("Body")
if not obj:
    print("[SculptMain] ❌ Objekt 'Body' nicht gefunden!")
    exit(1)

bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')

def apply_sculpt(param, factor, axis='Y'):
    print(f"[SculptMain][{param}] ▶️ Anwenden mit Wert {factor} auf Achse {axis}")
    idx = {'X': 0, 'Y': 1, 'Z': 2}.get(axis.upper(), 1)
    scale = 1 + ((factor - 50) / 50) * 0.5
    print(f"[SculptMain][{param}] Skaliere Faktor = {scale:.2f}")

    bpy.ops.mesh.select_all(action='SELECT')
    for v in obj.data.vertices:
        if param == "height" and idx == 2:
            v.co[idx] *= scale
        elif param == "breast_size" and v.co[0] > 0.2:
            v.co[idx] *= scale
        elif param == "hip_width" and v.co[2] < 0.5:
            v.co[idx] *= scale

bpy.ops.object.mode_set(mode='OBJECT')

# 🧠 Sculpting anwenden
apply_sculpt("height", data.get("height", 50), axis='Z')
apply_sculpt("breast_size", data.get("breast_size", 50), axis='Y')
apply_sculpt("hip_width", data.get("hip_width", 50), axis='X')

# 🔁 Symmetrie aktivieren?
sym = data.get("symmetry", True)
bpy.context.tool_settings.use_mesh_mirror_x = sym
print(f"[SculptMain] 🔁 Symmetrie {'aktiviert' if sym else 'deaktiviert'}")

# 💾 Vorschau als GLB
print(f"[SculptMain] ▶️ Exportiere GLB → {glb_output}")
bpy.ops.export_scene.gltf(filepath=glb_output, export_format='GLB')
print(f"[SculptMain] ✅ GLB gespeichert")

# 📸 Vorschau-Bild rendern
bpy.context.scene.render.filepath = preview_img_path
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"[SculptMain] ✅ Vorschau-Bild gespeichert: {preview_img_path}")

print("[SculptMain] ✅ Vorgang abgeschlossen.")