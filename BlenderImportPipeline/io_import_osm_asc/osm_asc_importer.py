import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty, FloatProperty, BoolProperty
from . import osmParser

def import_osm_file(self, filepath):
    print("Importing OSM file:", filepath)
    bpy.ops.import_scene.osm(filepath=filepath)

def import_asc_file(self, filepath):
    print("Importing ASC file:", filepath)
    bpy.ops.import_scene.asc(filepath=filepath)

# Operator
class OSM_ASC_OT_ImportOperator(Operator):
    """Create a scene from an OSM and ASC file"""
    bl_idname = "import_scene.osm_asc"
    bl_label = "Import OSM and ASC"
    bl_description = "Import an OSM and ASC file"
    bl_options = {'REGISTER', 'UNDO'}

    # filepath_osm: StringProperty(
    #     subtype="FILE_PATH", 
    #     name="OSM File"
    #     )
    # filepath_asc: StringProperty(
    #     subtype="FILE_PATH", 
    #     name="ASC File"
    #     )

    scalingFactor: FloatProperty(
        name="Scaling Factor",
        description="Scaling of the imported scene",
        default=10000,
        min=1,
        max=1000000,
        subtype='UNSIGNED',
    )

    storeyHeight: FloatProperty(
        name="Storey Height",
        description="Height of one storey",
        default=2.4,
        min=1,
        max=10,
        subtype='UNSIGNED'
    )

    highlightHFU: BoolProperty(
        name="Highlight HFU",
        description="Highlights HFU buildings",
        default=True
    )

    def execute(self, context):
        # osm_file = self.filepath_osm
        # asc_file = self.filepath_asc
        # Call the osmParser function with the OSM and ASC file paths
        # osmParser(osm_file, asc_file)
        print("parsing osm file")
        parser = osmParser.OSMParser(self.storeyHeight, self.scalingFactor, self.highlightHFU)
        parser.parse()


        return {'FINISHED'}

# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping

def register():
    bpy.utils.register_class(OSM_ASC_OT_ImportOperator)
    bpy.utils.register_manual_map(add_object_manual_map)
    #bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OSM_ASC_OT_ImportOperator)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    #bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

def menu_func_import(self, context):
    self.layout.operator(OSM_ASC_OT_ImportOperator.bl_idname, text="OpenStreetMap and ASC (.osm, .asc)")

if __name__ == "__main__":
    OSM_ASC_OT_ImportOperator()