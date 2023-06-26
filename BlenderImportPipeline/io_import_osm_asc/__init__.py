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
from . import osm_asc_importer

def menu_func_osm_asc_import(self, context):
    self.layout.operator(osm_asc_importer.OSM_ASC_OT_ImportOperator.bl_idname, text="OpenStreetMap (.osm) & Arc ASCII Grid (.asc)")

def register():
    bpy.utils.register_class(osm_asc_importer.OSM_ASC_OT_ImportOperator)
    bpy.utils.register_class(osm_asc_importer.OSM_ASC_PT_Panel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_osm_asc_import)
    bpy.utils.register_class(osm_asc_importer.OSM_ASC_Properties)
    bpy.types.Scene.osm_asc_props = bpy.props.PointerProperty(type=osm_asc_importer.OSM_ASC_Properties)

def unregister():
    bpy.utils.unregister_class(osm_asc_importer.OSM_ASC_OT_ImportOperator)
    bpy.utils.unregister_class(osm_asc_importer.OSM_ASC_PT_Panel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_osm_asc_import)
    bpy.utils.unregister_class(osm_asc_importer.OSM_ASC_Properties)
    del bpy.types.Scene.osm_asc_props

if __name__ == "__main__":
    register()