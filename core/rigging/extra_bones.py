class ExtraBoneHandler:
    def __init__(self):
        print("[ExtraBoneHandler][__init__] ▶️ Initialisierung...")
        print("[ExtraBoneHandler][__init__] ✅ ExtraBoneHandler bereit")

    def add_extra_bones(self, mesh_data, nsfw_enabled=True):
        print(f"[ExtraBoneHandler][add_extra_bones] ▶️ Eingabe: nsfw_enabled={nsfw_enabled}")
        bones = ["nipple.L", "nipple.R", "penis.base", "penis.tip"] if nsfw_enabled else []
        print(f"[ExtraBoneHandler][add_extra_bones] ✅ Füge folgende Extra-Bones hinzu: {bones}")
        return bones