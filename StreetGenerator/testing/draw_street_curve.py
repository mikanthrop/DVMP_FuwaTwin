from bpy.props import IntProperty
from bpy.types import Operator
import bpy
import math


bl_info = {
    "name": "Street Draw",
    "author": "Daniel Litterst and Leon Gobbert",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Add > Mesh > Test Draw",
    "description": "Adds a new Street Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def add_object(self, context):
    street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
    street_curve.dimensions = '3D'

    # switch all open 3d views to view scene from top -> drawn street lays on ground
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            override = bpy.context.copy()
            override["area"] = area
            bpy.ops.view3d.view_axis(override, type='TOP', align_active=False) 
            if  area.spaces.active.region_3d.is_perspective:
                bpy.ops.view3d.view_persportho(override)
            else:
                pass

    # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    street_curve.fill_mode = 'HALF'
    # Breadth of extrusion, modified by lanes
    street_curve.extrude = 0.03 * self.lanes
    # create object out of curve
    obj = bpy.data.objects.new('Street', street_curve)
    # link to scene-collection and select obj
    collection = bpy.data.collections.get('Collection')
    if (collection):
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)

    # Set the context for the operator
    bpy.context.view_layer.objects.active = obj
    # Toggle to Edit Mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.wm.tool_set_by_id(name="builtin.draw")
    
    # tilt
    # Define a custom handler function to apply the tilt
    def handle_spline_draw(context):
        # Access the active object (the drawn splines)
        for curve in bpy.data.curves:

            if curve == street_curve:
                for spline in curve.splines:
                    
                    if spline.type != 'BEZIER':
                        print('only bezier splines allowed')
                        continue
                    
                    total_points = len(spline.bezier_points)
                    if total_points == 0:
                        continue
                    
                    # Iterate over each point in the spline
                    for point in spline.bezier_points:
                        # Modify the tilt by 90 degrees
                        point.tilt = 1.5708  # 90 degrees in radians
        

    # Register the handler function
    bpy.app.handlers.depsgraph_update_post.append(handle_spline_draw)
    # material
    assign_road_material(self.lanes)


def build_geometry_nodes():
    return

def assign_road_material(lanes):
    road_mat = bpy.data.materials.new("Road Material")
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    imgpath = "C:/Users/Le_go/Documents/GitHub/DVMP_FuwaTwin/StreetGenerator/draw_tool_build/textures/Road_texture.jpg"
    img = bpy.data.images.load(imgpath)

    principled_BSDF = nodes.get('Principled BSDF')
    tex_node: bpy.types.Node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    
    road_mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])
    bpy.context.object.data.materials.append(road_mat)


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Draw Street Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    OBJECT_OT_add_object()