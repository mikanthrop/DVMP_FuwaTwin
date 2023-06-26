import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty #, StringProperty
from . import osmParser

# Operator
class OSM_ASC_OT_ImportOperator(Operator):
    """Create a scene from an OSM and ASC file"""
    bl_idname = "import_scene.osm_asc"
    bl_label = "Import OSM and ASC"
    bl_description = "Imports an OSM and ASC file"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

    scalingFactor: FloatProperty(
        name="Scaling Factor",
        description="Scaling of the imported scene",
        default=10000,
        min=1,
        max=1000000,
    )

    storeyHeight: FloatProperty(
        name="Storey Height",
        description="Height of one storey",
        default=2.4,
        min=1,
        max=10,
    )

    highlightHFU: BoolProperty(
        name="Highlight HFU",
        description="Highlights HFU buildings",
        default=True
    )

    def execute(self, context):
        # props = context.window_manager.osm_asc_props
        
        storey_height = self.storeyHeight
        scaling_factor = self.scalingFactor
        highlight_hfu = self.highlightHFU
        parser = osmParser.OSMParser(storey_height, scaling_factor, highlight_hfu)
        parser.parse()
        return {'FINISHED'}

# class OSM_ASC_PT_Panel(Panel):
#     bl_idname = "OSM_ASC_PT_Panel"
#     bl_label = "OSM and ASC Importer"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Tool'

#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         operator = scene.operator("import_scene.osm_asc")
#         box = layout.box()

#         box.prop(operator, "storeyHeight")
#         box.prop(operator, "scalingFactor")
#         box.prop(operator, "highlightHFU")
#         box.operator("import_scene.osm_asc", text="Import")

# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping
