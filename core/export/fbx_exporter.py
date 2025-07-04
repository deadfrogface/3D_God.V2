import os

class FBXExporter:
    def __init__(self, export_dir="exports/"):
        print(f"[FBXExporter][__init__] ▶️ Eingabe: export_dir={export_dir}")
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)
        print("[FBXExporter][__init__] ✅ Exportverzeichnis angelegt oder bereits vorhanden")

    def export(self, character_data):
        print(f"[FBXExporter][export] ▶️ Eingabe: character_data={character_data}")
        name = character_data.get("name", "export")
        filename = f"{name.lower().replace(' ', '_')}.fbx"
        path = os.path.join(self.export_dir, filename)

        try:
            # Stub: Simulierter Export
            with open(path, 'w') as f:
                f.write(f"# Simulierter FBX Export für: {name}\n")
                f.write(str(character_data))
            print(f"[FBXExporter][export] ✅ Export erfolgreich: {path}")
            return path
        except Exception as e:
            print(f"[FBXExporter][export] ❌ Fehler beim Export: {e}")
            return None