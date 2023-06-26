bl_info = {
    "name": "OSM and ASC Map with Terrain Import Mockup",
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
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import FloatProperty, BoolProperty
from . import osmParser

class OSM_ASC_Properties(PropertyGroup):
    """Properties for the OSM and ASC import"""
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
        max=100,
    )

    highlightHFU: BoolProperty(
        name="Highlight HFU",
        description="Highlights HFU buildings",
        default=True
    )

class OSM_ASC_OT_ImportOperator(Operator):
    """Create a scene from an OSM and ASC file"""
    bl_idname = "import_scene.osm_asc"
    bl_label = "Import OSM and ASC"
    bl_description = "Imports an OSM and ASC file"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.osm_asc_props

        storey_height = props.storeyHeight
        scaling_factor = props.scalingFactor
        highlight_hfu = props.highlightHFU
        parser = osmParser.OSMParser(storey_height, scaling_factor, highlight_hfu)
        parser.parse()
        return {'FINISHED'}
    

class OSM_ASC_PT_Panel(Panel):
    """Creates a Sidepanel in the 3D View"""
    bl_idname = "OSM_ASC_PT_Panel"
    bl_label = "OSM and ASC Importer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'OSM & ASC Importer'

    def draw(self, context):
        layout = self.layout
        props = context.scene.osm_asc_props
        
        layout.row().label(text="FuWaTwin Config")
        layout.prop(props, "storeyHeight")
        layout.prop(props, "scalingFactor")
        layout.prop(props, "highlightHFU")
        
        self.layout.separator()
        layout.row().operator("import_scene.osm_asc", text="Import")