import bpy
import sys

# Finde Argument (Name)
args = sys.argv
export_name = "exported_character"
if "--" in args:
    idx = args.index("--")
    if idx + 1 < len(args):
        export_name = args[idx + 1]

print(f"[Blender] Exportiere nach exports/{export_name}.fbx")

# Wähle alles aus und exportiere (Demo)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=f"exports/{export_name}.fbx", use_selection=True)