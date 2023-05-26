# https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# https://www.youtube.com/watch?v=Ve9h7-E8EuM
# https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# Missing (for the street to have basic functionality):
# -Allow users to reopen the properties panel
# -Scaling of Street-Curve
# -Name of Object
# -extrude along Y-Axis

import math
from mathutils import geometry, Vector, Matrix
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty, IntProperty
from bpy.types import Operator
import bpy
import os
import glob


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


# Deko-Objekte an Bezier Punkten spawnen
# ...oder an Kuve entlang, wenns geht
# ggf. Sachen an einem Punkt spawnen und selbst setzten lassen


def add_object(self):

    # # Create curve object
    # street_curve = bpy.data.curves.new('BezierCurve', 'CURVE')
    # street_curve.dimensions = '3D'

    # # Create a new spline for the curve
    # spline = street_curve.splines.new('BEZIER')
    # bezier_points_array = [(0.0, 0.0, -2.0), (0.0,  0.0, -1.0), (0.0,  0.0, 0.0), (0.0,  0.0, 1.0), (0.0,  0.0, 2.0)]
    # spline.bezier_points.add(len(bezier_points_array) + 1)
    # for i in range(len(bezier_points_array)):
    #     spline.bezier_points[i].co = bezier_points_array[i]
    #     spline.bezier_points[i].handle_left = bezier_points_array[i].z - 0.1    
    #     spline.bezier_points[i].handle_ringht = bezier_points_array[i].z + 0.1

    # define_control_points(self.start_point, self.end_point, spline)

    # # Which parts of the curve to extrude ['HALF', 'FRONT', 'BACK', 'FULL'].
    # street_curve.fill_mode = 'HALF'
    # # Breadth of extrusion, modified by lanes
    # street_curve.extrude = 0.125 * self.lanes
    # # create object out of curve
    # obj = bpy.data.objects.new('StreetObject', street_curve)
    # # Tilt curve by 90 degrees
    # obj.rotation_euler[0] = math.radians(90)
    # Set origin right between start and end points (How tf does it work?!)


    # # Create bezier circle and randomize.
    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True)
    bpy.ops.curve.subdivide(number_cuts=8)
    # bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0, seed=0)
    bpy.ops.transform.resize(value=(2.0, 2.0, 3.5))
    bpy.ops.object.mode_set(mode='OBJECT')
    curve = bpy.context.active_object
    

    # create Tree
    # Specify the path to your .obj file
    # file_path = "Tree.obj"
    # bpy.ops.wm.obj_import(filepath="C:\\GitHub\\DVMP_FuwaTwin\\StreetGenerator\\Tree.obj", directory="C:\\GitHub\\DVMP_FuwaTwin\\StreetGenerator\\", files=[{"name":"Tree.obj", "name":"Tree.obj"}])

    # Create cube.
    bpy.ops.mesh.primitive_cube_add(calc_uvs=True, size=0.1)
    # bpy.ops.object.shade_smooth()
    cube = bpy.context.active_object
    cube.scale = (0.2, 0.2, 0.2)

    # bpy.ops.mesh.primitive_plane_add(calc_uvs=True)
    # plane = bpy.context.active_object
    # cube.parent = plane
    
    # Append modifiers.
    array_mod = cube.modifiers.new(name='Array', type='ARRAY')
    curve_mod = cube.modifiers.new(name='Curve', type='CURVE')
    # bevel_mod = cube.modifiers.new(name='Bevel', type='BEVEL')
    
    # Array modifier properties.
    array_mod.fit_type = 'FIT_CURVE'
    array_mod.curve = curve
    array_mod.use_relative_offset = True
    array_mod.relative_offset_displace = (1.25, 0.0, 0.0) # Adjust the offset values here (x, y, z).
    
    # Curve modifier properties.
    curve_mod.object = curve
    curve_mod.deform_axis = 'POS_X'

    # plane.instance_type = 'FACES'
    
    # # Bevel modifier properties.
    # bevel_mod.segments = 2
    # bevel_mod.offset_type = 'PERCENT'
    # bevel_mod.width = 10.0
    # link to scene-collection

    # collection = bpy.data.collections.get('Collection')
    # if (collection):
    #     collection.objects.link(obj)
    # else:
    #     bpy.context.scene.collection.objects.link(obj)


def get_unit_vec(start, end, factor):
    vec = end - start
    vec_len = math.sqrt(math.pow(vec.x, 2) +
                        math.pow(vec.y, 2)+math.pow(vec.z, 2))
    if (vec_len == 0):
        return (0, 0, 0)
    else:
        unit_vec = vec / vec_len
        return unit_vec*factor


class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

    start_point: FloatVectorProperty(
        name="Start Point",
        default=(0.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should begin",
    )
    end_point: FloatVectorProperty(
        name="End Point",
        default=(4.0, 0.0, 0.0),
        subtype='XYZ',
        description="Choose a point where the street should end",
    )
    lanes: IntProperty(
        name="Lanes",
        description="Number of lanes the street should have",
        default=1,
        min=1,
        max=4,
        subtype='UNSIGNED',
    )
    cuts: IntProperty(
        name="Control Points",
        description="Number of control points between start and end point",
        default=2,
        min=1,
        max=100,
        subtype='UNSIGNED',
    )

    def execute(self, context):
        add_object(self)
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


# # https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# # https://www.youtube.com/watch?v=Ve9h7-E8EuM
# # https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# # source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# # Missing (for the street to have basic functionality):
# # -Allow users to reopen the properties panel
# # -Scaling of Street-Curve
# # -Name of Object
# # -extrude along Y-Axis


# from mathutils import geometry
# from mathutils import Vector
# from bpy_extras.object_utils import AddObjectHelper, object_data_add
# from bpy.props import FloatVectorProperty, IntProperty
# from bpy.types import Operator
# import bpy


# bl_info = {
#     "name": "Street Generator",
#     "author": "Daniel Litterst and Leon Gobbert",
#     "version": (1, 0),
#     "blender": (3, 5, 0),
#     "location": "View3D > Add > Mesh > New Object",
#     "description": "Adds a new Street Object",
#     "warning": "",
#     "doc_url": "",
#     "category": "Add Mesh",
# }


# def add_object(self, context):
#     scale_x = self.scale.x
#     scale_y = self.scale.y
#     cuts = self.cuts

#     verts = [
#         Vector((-1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, -1 * scale_y, 0)),
#         Vector((-1 * scale_x, -1 * scale_y, 0)),
#     ]

#     edges = []
#     faces = [[0, 1, 2, 3]]

#     res_per_section = 6
#     interpolate_bezier = geometry.interpolate_bezier
#     ops_curve = bpy.ops.curve
#     ops_mesh = bpy.ops.mesh

#     # Create a curve, subdivide and randomize it.
#     ops_curve.primitive_bezier_curve_add(enter_editmode=True)
#     ops_curve.subdivide(number_cuts=cuts)
#     # bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.01, seed=0)

#     # After randomizing the curve, recalculate its normals so
#     # the cubes calculated by interpolate bezier will be more
#     # evenly spaced.
#     ops_curve.select_all(action='SELECT')
#     ops_curve.normals_make_consistent(calc_length=True)

#     # Switch back to object mode and cache references to the curve
#     # and its bezier points.
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bez_curve = bpy.context.active_object
#     bez_points = bez_curve.data.splines[0].bezier_points

#     # Create an empty list.
#     points_on_curve = []

#     # Loop through the bezier points in the bezier curve.
#     bez_len = len(bez_points)
#     i_range = range(1, bez_len, 1)
#     for i in i_range:

#         # Cache a current and next point.
#         curr_point = bez_points[i - 1]
#         next_point = bez_points[i]

#         # Calculate bezier points for this segment.
#         calc_points = interpolate_bezier(
#             curr_point.co,
#             curr_point.handle_right,
#             next_point.handle_left,
#             next_point.co,
#             res_per_section + 1)

#         # The last point on this segment will be the
#         # first point on the next segment in the spline.
#         if i != bez_len - 1:
#             calc_points.pop()

#         # Concatenate lists.
#         points_on_curve += calc_points

#         # Create an empty parent under which cubes will be placed.

#         # For each point created by interpolate bezier, create a cube.
#         cube_rad = 1.5 / (res_per_section * bez_len)
#         for point in points_on_curve:
#             bpy.ops.object.empty_add(type='PLAIN_AXES', location=bez_curve.location)
#             group = bpy.context.active_object
#             # point_translation = bpy.context.object.matrix_local.to_translation()
#             # ops_mesh.primitive_cube_add(location=point, size=0.1, rotation=point)
#             ops_mesh.primitive_cube_add(location=point, size=0.1)

#             # ops_mesh.primitive_cube_add(radius=cube_rad, location=point)
#             cube = bpy.context.active_object
#             cube.parent = bez_curve


# class OBJECT_OT_add_object(Operator):
#     """Create a new Street Object"""
#     bl_idname = "mesh.add_object"
#     bl_label = "Add Street Object"
#     bl_options = {'REGISTER', 'UNDO'}

#     scale: FloatVectorProperty(
#         name="Scale",
#         default=(1.0, 1.0, 1.0),
#         subtype='TRANSLATION',
#         description="scaling",
#     )
#     cuts: IntProperty(
#         name="Cuts",
#         description="Number of cuts along the street",
#         default=1,
#         min=0,
#         max=100,
#         subtype='UNSIGNED'
#     )
    


#     def execute(self, context):
#         add_object(self, context)
#         return {'FINISHED'}

# # def bezier_tangent(pt0=Vector(), pt1=Vector(), pt2=Vector(), pt3=Vector(), step=0.5):
# #     # Return early if step is out of bounds [0, 1].
# #     if step <= 0.0:
# #         return pt1 - pt0
# #     if step >= 1.0:
# #         return pt3 - pt2

# #     # Find coefficients.
# #     u = 1.0 - step
# #     ut6 = u * step * 6.0
# #     tsq3 = step * step * 3.0
# #     usq3 = u * u * 3.0

# #     # Find tangent and return.
# #     return (pt1 - pt0) * usq3 + (pt2 - pt1) * ut6 + (pt3 - pt2) * tsq3

# # Registration
# def add_object_button(self, context):
#     self.layout.operator(
#         OBJECT_OT_add_object.bl_idname,
#         text="Add Street Object",
#         icon='PLUGIN')


# # This allows you to right click on a button and link to documentation
# def add_object_manual_map():
#     url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
#     url_manual_mapping = (
#         ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
#     )
#     return url_manual_prefix, url_manual_mapping


# def register():
#     bpy.utils.register_class(OBJECT_OT_add_object)
#     bpy.utils.register_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


# def unregister():
#     bpy.utils.unregister_class(OBJECT_OT_add_object)
#     bpy.utils.unregister_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


# if __name__ == "__main__":
#     register()


# # https://blender.stackexchange.com/questions/278948/coons-patch-bezier-curve
# # https://www.youtube.com/watch?v=Ve9h7-E8EuM
# # https://www.youtube.com/watch?v=aVwxzDHniEw&t=143s
# # source (bc. I can't come up with that shit on my own...| me neighter): https://behreajj.medium.com/scripting-curves-in-blender-with-python-c487097efd13
# # Missing (for the street to have basic functionality):
# # -Allow users to reopen the properties panel
# # -Scaling of Street-Curve
# # -Name of Object
# # -extrude along Y-Axis

# from mathutils import geometry, Vector, Matrix
# from bpy_extras.object_utils import AddObjectHelper, object_data_add
# from bpy.props import FloatVectorProperty, IntProperty
# from bpy.types import Operator
# import bpy


# bl_info = {
#     "name": "Street Generator",
#     "author": "Daniel Litterst and Leon Gobbert",
#     "version": (1, 0),
#     "blender": (3, 5, 0),
#     "location": "View3D > Add > Mesh > New Object",
#     "description": "Adds a new Street Object",
#     "warning": "",
#     "doc_url": "",
#     "category": "Add Mesh",
# }


# def add_object(self, context):
#     scale_x = self.scale.x
#     scale_y = self.scale.y
#     cuts = self.cuts

#     verts = [
#         Vector((-1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, 1 * scale_y, 0)),
#         Vector((1 * scale_x, -1 * scale_y, 0)),
#         Vector((-1 * scale_x, -1 * scale_y, 0)),
#     ]

#     edges = []
#     faces = [[0, 1, 2, 3]]

#     res_per_section = 6
#     interpolate_bezier = geometry.interpolate_bezier
#     ops_curve = bpy.ops.curve
#     ops_mesh = bpy.ops.mesh

#     # Create a curve, subdivide and randomize it.
#     ops_curve.primitive_bezier_curve_add(enter_editmode=True)
#     ops_curve.subdivide(number_cuts=cuts)

#     # After randomizing the curve, recalculate its normals so
#     # the cubes calculated by interpolate bezier will be more
#     # evenly spaced.
#     ops_curve.select_all(action='SELECT')
#     ops_curve.normals_make_consistent(calc_length=True)

#     # Switch back to object mode and cache references to the curve
#     # and its bezier points.
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bez_curve = bpy.context.active_object
#     bez_points = bez_curve.data.splines[0].bezier_points

#     # Create an empty list.
#     points_on_curve = []

#     # Loop through the bezier points in the bezier curve.
#     bez_len = len(bez_points)
#     i_range = range(1, bez_len, 1)

#     for i in i_range:

#         # Cache a current and next point.
#         curr_point = bez_points[i - 1]
#         next_point = bez_points[i]

#         # Calculate bezier points for this segment.
#         calc_points = interpolate_bezier(
#             curr_point.co,
#             curr_point.handle_right,
#             next_point.handle_left,
#             next_point.co,
#             res_per_section + 1)

#         # The last point on this segment will be the
#         # first point on the next segment in the spline.
#         if i != bez_len - 1:
#             calc_points.pop()

#         # Concatenate lists.
#         points_on_curve += calc_points

#         # Create an empty parent under which cubes will be placed.
#         bpy.ops.object.empty_add(
#             type='PLAIN_AXES', location=bez_curve.location)
#         group = bpy.context.active_object

#         # For each point created by interpolate bezier, create a cube.
#         cube_rad = 1.5 / (res_per_section * bez_len)
#         # Align the cubes with the tangent of the spline
#         for point in points_on_curve:
#             ops_mesh.primitive_cube_add(location=point, size=0.1)
#             cube = bpy.context.active_object
#             cube.parent = group

#             # Get the tangent vector at the current point
#             spline = bez_curve.data.splines[0]
#             tangent = Vector()
#             if spline.type == 'BEZIER':
#                 i = int(point[0] * (len(spline.bezier_points) - 1))
#                 handle_left = spline.bezier_points[i].handle_left
#                 handle_right = spline.bezier_points[i].handle_right
#                 tangent = handle_right - handle_left
#             else:
#                 i = int(point[0] * (len(spline.points) - 1))
#                 p1 = spline.points[i].co
#                 p2 = spline.points[i + 1].co
#                 tangent = p2 - p1
#             t = tangent.normalized()

#             # Calculate the rotation matrix to align the cube with the tangent
#             up = Vector((0, 0, 1))
#             axis = up.cross(t)
#             angle = up.angle(t)
#             matrix = Matrix.Rotation(angle, 4, axis)

#             # Apply the rotation to the cube
#             cube.matrix_world = matrix @ cube.matrix_world


# class OBJECT_OT_add_object(Operator):
#     """Create a new Street Object"""
#     bl_idname = "mesh.add_object"
#     bl_label = "Add Street Object"
#     bl_options = {'REGISTER', 'UNDO'}

#     scale: FloatVectorProperty(
#         name="Scale",
#         default=(1.0, 1.0, 1.0),
#         subtype='TRANSLATION',
#         description="scaling",
#     )
#     cuts: IntProperty(
#         name="Cuts",
#         description="Number of cuts along the street",
#         default=1,
#         min=0,
#         max=100,
#         subtype='UNSIGNED'
#     )

#     def execute(self, context):
#         add_object(self, context)
#         return {'FINISHED'}

# # Registration


# def add_object_button(self, context):
#     self.layout.operator(
#         OBJECT_OT_add_object.bl_idname,
#         text="Add Street Object",
#         icon='PLUGIN')


# # This allows you to right click on a button and link to documentation
# def add_object_manual_map():
#     url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
#     url_manual_mapping = (
#         ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
#     )
#     return url_manual_prefix, url_manual_mapping


# def register():
#     bpy.utils.register_class(OBJECT_OT_add_object)
#     bpy.utils.register_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


# def unregister():
#     bpy.utils.unregister_class(OBJECT_OT_add_object)
#     bpy.utils.unregister_manual_map(add_object_manual_map)
#     bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


# if __name__ == "__main__":
#     register()
