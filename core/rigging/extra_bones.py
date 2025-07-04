from core.logger import log

class ExtraBoneHandler:
    def __init__(self):
        log.info("[ExtraBoneHandler][__init__] ▶️ Initialisierung...")
        log.success("[ExtraBoneHandler][__init__] ✅ ExtraBoneHandler bereit")

    def add_extra_bones(self, mesh_data, nsfw_enabled=True):
        log.info(f"[ExtraBoneHandler][add_extra_bones] ▶️ Eingabe: nsfw_enabled={nsfw_enabled}")
        bones = ["nipple.L", "nipple.R", "penis.base", "penis.tip"] if nsfw_enabled else []
        log.success(f"[ExtraBoneHandler][add_extra_bones] ✅ Füge folgende Extra-Bones hinzu: {bones}")
        return bones