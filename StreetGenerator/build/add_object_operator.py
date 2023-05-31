import bpy
from bpy.props import IntProperty
from bpy.types import Operator
from . import helper_functions


def add_object(self):
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.editmode_toggle()
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
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.transform.tilt(value=1.5708, mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
                            proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False)
        # material
        helper_functions.assign_road_material(self.lanes)

class OBJECT_OT_add_object(Operator):
    """Create a new Street Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Street Object"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self) -> None:
        super().__init__()

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