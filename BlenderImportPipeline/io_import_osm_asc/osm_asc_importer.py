import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty, FloatProperty
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

    filepath_osm: StringProperty(
        subtype="FILE_PATH", 
        name="OSM File"
        )
    filepath_asc: StringProperty(
        subtype="FILE_PATH", 
        name="ASC File"
        )

    scalingFactor: FloatProperty(
        name="Scaling Factor",
        description="Scaling of the imported scene",
        default=10000,
        min=1,
        max=1000000,
        subtype='UNSIGNED',
    )

    def execute(self, context):
        # osm_file = self.filepath_osm
        # asc_file = self.filepath_asc
        print("parsing osm file")
        parser = osmParser.OSMParser()
        parser.parse()

        # Call the osmParser function with the OSM and ASC file paths
        # osmParser(osm_file, asc_file)

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(OSM_ASC_OT_ImportOperator.bl_idname, text="OpenStreetMap and ASC (.osm, .asc)")
