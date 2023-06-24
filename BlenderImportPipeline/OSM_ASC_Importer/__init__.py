bl_info = {
    "name": "OSM and ASC Map with Terrain Import",
    "author": "Alexander Weibert, Hau-David Nguyen, Marie Cleppien",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "location": "File > Import > OSM (.osm)",
    "description": "Imports Open Street View Map into Blender",
    "warning": "",
    "doc_url": "",
    "category": "Import",
}

import bpy
from .osm_asc_importer import OSM_ASC_OT_ImportOperator
from .osm_asc_importer import IMPORT_PT_ImportPanel

def menu_func_osm_asc_import(self, context):
    self.layout.operator(OSM_ASC_OT_ImportOperator.bl_idname, text="OpenStreetMap (.osm) & Arc ASCII Grid (.asc)")

# def menu_func_asc_import(self, context):
#     self.layout.operator(ASC_OT_ImportOperator.bl_idname, text="Arc ASCII Grid (.asc)")

def register():
    bpy.utils.register_class(OSM_ASC_OT_ImportOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_osm_asc_import)
    bpy.utils.register_class(IMPORT_PT_ImportPanel)
    
def unregister():
    bpy.utils.unregister_class(OSM_ASC_OT_ImportOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_osm_asc_import)
    bpy.utils.unregister_class(IMPORT_PT_ImportPanel)

if __name__ == "__main__":
    register()