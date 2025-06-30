class ExtraBoneHandler:
    def __init__(self):
        print("🧩 ExtraBoneHandler bereit")

    def add_extra_bones(self, mesh_data, nsfw_enabled=True):
        bones = ["nipple.L", "nipple.R", "penis.base", "penis.tip"] if nsfw_enabled else []
        print("➕ Füge folgende Extra-Bones hinzu:", bones)
        return bones
