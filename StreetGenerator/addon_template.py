from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty
from bpy.types import Operator
import bpy

# Missing!: Allow users to reopen the properties panel

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
    rotation = (self.rot_vec.x,
                self.rot_vec.y, self.rot_vec.z)

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    street_mesh = bpy.data.meshes.new(name="New Street Mesh")
    street_mesh.from_pydata(verts, edges, faces)
    street_object = bpy.data.objects.new("Street", street_mesh)
    street_object.rotation_euler = rotation
    bpy.data.collections["Collection"].objects.link(street_object)


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
    rot_vec: FloatVectorProperty(
        name='Rotation',
        default=(0, 0, 0),
        subtype='EULER',
        description='rotate the mesh',
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
    OBJECT_OT_add_object()
