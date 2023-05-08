# source (bc. I can't come up with that shit on my own...): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis


from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty, IntProperty
from bpy.types import Operator
import bpy


bl_info = {
    "name": "Street Generator",
    "author": "Daniel Litterst and Leon Gobbert",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Street Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y
    cuts = self.cuts

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
    bpy.ops.curve.subdivide(number_cuts=cuts)
    street_curve = bpy.ops.curve
    # Store a shortcut to the curve object's data.
    obj_data = bpy.context.active_object.data
    # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    # obj_data.fill_mode = 'HALF'
    # Breadth of extrusion.
    # obj_data.extrude = 0.125cuts
    # Smoothness of the segments on the curve.
    obj_data.resolution_u = 20
    obj_data.render_resolution_u = 32
    bpy.ops.object.mode_set(mode='OBJECT')


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="Scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )
    cuts: IntProperty(
        name="Cuts",
        description="Number of cuts along the street",
        default=1,
        min=0,
        max=100,
        subtype='UNSIGNED'
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Street Object",
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
    register()
