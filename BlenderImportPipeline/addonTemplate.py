import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty


bl_info = {
    "name": "OSM Map Import",
    "author": "Alexander Weibert, Hau-David Nguyen, Marie Cleppien",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "File > Import > OSM (.osm)",
    "description": "Imports Open Street View Map into Blender",
    "warning": "",
    "doc_url": "",
    "category": "Import",
}

def import_osm_file(self, filepath):
        print("Importing OSM file:", filepath)
        # Clear existing objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        # Import OSM file
        bpy.ops.import_scene.osm(filepath=filepath)


# Operator
class OSM_IMPORT(Operator):
    """OSM File Import"""
    bl_idname = "import_scene.osm"
    bl_label = "Import OSM."
    bl_description = "Import an OSM file."
    bl_options = {'REGISTER', 'UNDO'}
    filepath: StringProperty(subtype="FILE_PATH")

    
    def execute(self, context):
        if self.filepath:
           osm_file = import_osm_file(self.filepath)
           # parse osm_file using osmParser
        else:
            self.report({'ERROR'}, "Invalid OSM file path")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Panel
class OSM_IMPORT_PANEL(Panel):
    bl_idname = "OSM_PT_osm_import_panel"
    bl_label = "OSM Import"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Import OSM File:")
        row.operator("import_scene.osm", icon='FILE_FOLDER')
        

# Register
classes = [
    OSM_IMPORT,
    OSM_IMPORT_PANEL,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

#def register():
#    bpy.utils.register_class(OSM_IMPORT)
#    bpy.utils.register_manual_map(add_object_manual_map)
#    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


#def unregister():
#    bpy.utils.unregister_class(OSM_IMPORT)
#    bpy.utils.unregister_manual_map(add_object_manual_map)
#    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)