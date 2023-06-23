import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty
from . import osmParser


def import_osm_file(self, filepath):
    print("Importing OSM file:", filepath)
    bpy.ops.import_scene.osm(filepath=filepath)

def import_asc_file(filepath):
    print("Importing ASC file:", filepath)
    bpy.ops.import_scene.asc(filepath=filepath)

# Operator
class OSM_OT_ImportOperator(Operator):
    """Import a OSM File"""
    bl_idname = "import_scene.osm"
    bl_label = "Import OSM."
    bl_description = "Import an OSM file."
    bl_options = {'REGISTER', 'UNDO'}
    filepath: StringProperty(subtype="FILE_PATH")

    
    def execute(self, context):
        if self.filepath:
            osm_file = import_osm_file(self.filepath)
            osmParser.parse(osm_file)
        else:
            self.report({'ERROR'}, "Invalid OSM file path")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
# Operator
class ASC_OT_ImportOperator(Operator):
    """Import a ASC File"""
    bl_idname = "import_scene.asc"
    bl_label = "Import ASC."
    bl_description = "Import an ASC file."
    bl_options = {'REGISTER', 'UNDO'}
    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if self.filepath.lower().endswith('.asc'):
            import_asc_file(self.filepath)
        else:
            self.report({'ERROR'}, "Invalid ASC file path")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Panel
class IMPORT_PT_ImportPanel(Panel):
    bl_idname = "IMPORT_PT_import_panel"
    bl_label = "Import ASC and OSM Files."
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Import OSM File:")
        row.operator("import_scene.osm", icon='FILE_FOLDER')
        
        row = layout.row()
        row.label(text="Import ASC File:")
        row.operator("import_scene.asc", icon='FILE_FOLDER')

# Register
# classes = [
#     OSM_IMPORT,
#     ASC_IMPORT,
#     IMPORT_PANEL
# ]

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)


# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#     register()