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
    bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.transform.tilt(value=1.5708, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
                           proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False)
    bpy.ops.wm.tool_set_by_id(name="builtin.draw")

    # delete primitive curves' vertices, so only the drawn splines of the user will be used
    bpy.ops.curve.delete(type='VERT')

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
    bpy.context.object.data.fill_mode = 'HALF'
    # Breadth of extrusion, modified by lanes
    bpy.context.object.data.extrude = 0.03 * self.lanes
    # rename
    # .....
    # tilt
    # material
    assign_road_material(self.lanes)
    

def assign_road_material(lanes):
    road_mat = bpy.data.materials.new("Road Material")
    road_mat.use_nodes = True
    nodes = road_mat.node_tree.nodes

    imgpath = "/Users/leonprivat/Documents/GitHub/DVMP_FuwaTwin/StreetGenerator/build/textures/Road_texture.jpg"
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