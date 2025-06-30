from .nsfw_manager import NSFWManager
from .preset_handler import PresetHandler
from core.rigging.auto_rigger import AutoRigger
from core.rigging.metahuman_skeleton import MetahumanSkeleton
from core.rigging.extra_bones import ExtraBoneHandler
from core.export.fbx_exporter import FBXExporter
from core.export.preset_saver import PresetSaver
from core.sculpting.blender_bridge import BlenderBridge
from core.sculpting.sculpt_tools import SculptTools

class CharacterSystem:
    def __init__(self):
        self.nsfw_manager = NSFWManager()
        self.preset_handler = PresetHandler()
        self.auto_rigger = AutoRigger()
        self.meta_skeleton = MetahumanSkeleton()
        self.extra_bones = ExtraBoneHandler()
        self.exporter = FBXExporter()
        self.preset_saver = PresetSaver()
        self.sculpt_tools = SculptTools()
        self.blender = BlenderBridge()

        self.current_data = {
            "name": "Unbenannt",
            "gender": "unknown",
            "race": "human",
            "attributes": {},
            "assets": []
        }

    def set_nsfw_mode(self, enabled: bool):
        self.nsfw_manager.toggle_nsfw(enabled)

    def is_nsfw(self):
        return self.nsfw_manager.is_visible()

    def load_preset(self, name: str):
        data = self.preset_handler.load_preset(name)
        if data:
            self.current_data = data
            return True
        return False

    def save_preset(self, name: str):
        self.preset_handler.save_preset(name, self.current_data)

    def get_current_data(self):
        return self.current_data

    def set_current_data(self, data: dict):
        self.current_data = data

    def rig_character(self):
        return self.auto_rigger.apply_auto_rig(self.current_data)

    def add_nsfw_bones(self):
        return self.extra_bones.add_extra_bones({}, self.is_nsfw())

    def convert_to_ue5(self):
        return self.meta_skeleton.convert_to_metahuman({})

    def export_to_file(self):
        return self.exporter.export(self.current_data)

    def save_current_as_preset(self):
        return self.preset_saver.save(self.current_data)

    def sculpt(self):
        self.sculpt_tools.start_sculpt_session()

    def run_blender_script(self, script, args=None):
        return self.blender.run_blender_script(script, args)
